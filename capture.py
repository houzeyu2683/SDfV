import os
import glob
import pathlib
import moviepy.editor
import retinaface.RetinaFace
import tensorflow
import numpy
import PIL.Image
import multiprocessing
import argparse
import facenet_pytorch
import torch

def getAngle(x, y):
    product = numpy.dot(x, y)
    u = numpy.linalg.norm(x)
    v = numpy.linalg.norm(y)
    theta = numpy.arccos(product / (u * v))
    angle = numpy.degrees(theta)
    return(angle)

def getError(x, y):
    comparison = numpy.array(x) - numpy.array(y)
    error = numpy.absolute(comparison).sum()
    return(error)



class Agent:

    def __init__(self):
        return

    def makeModel(self):
        experiment = tensorflow.config.experimental
        for item in experiment.list_physical_devices('GPU'):
            experiment.set_memory_growth(item, True)
            _ = experiment.list_logical_devices('GPU')
            continue
        self.model = retinaface.RetinaFace
        return

    def getBox(self, frame, boundary):
        height, width, _ = frame.shape
        # response = retinaface.RetinaFace.detect_faces(frame)
        response = self.model.detect_faces(frame)
        if(len(response)!=1): return
        area = response['face_1']['facial_area']
        mark = response['face_1']["landmarks"]
        x = numpy.array(mark["left_eye"]) - numpy.array(mark['nose'])
        y = numpy.array(mark["right_eye"]) - numpy.array(mark['nose'])
        angle = getAngle(x, y)
        if(angle<60 or angle>100): return
        if(boundary):
            scale = 1.0
            box = [
                max(0, area[0]-int((area[2]- area[0])*scale)),
                max(0, area[1]-int((area[3]- area[1])*scale)),
                min(width, area[2]+int((area[2]- area[0])*scale)),
                min(height, area[3]+int((area[3]- area[1])*scale))
            ]
            pass
        else: box = area
        return(box)

    def getHead(self, video, interval):
        delta = None
        video = video.subclip(interval[0], interval[1])
        progress = video.iter_frames(with_times=True)
        for index, (time, frame) in enumerate(progress):
            if(index % 25!=0): continue
            box = self.getBox(frame=frame, boundary=False)
            if(box==None): continue
            delta = time
            break
        head = int(interval[0] + delta) if(delta!=None) else -1
        return(head)

    def getTail(self, video, interval):
        delta = None
        video = video.subclip(interval[0], interval[1])
        progress = video.iter_frames(with_times=True)
        for index, (time, frame) in enumerate(progress):
            if(index==0):
                history = self.getBox(frame=frame, boundary=False)
                if(history==None): 
                    tail = int(interval[0])
                    return(tail)
                continue
            if(index % 4!=0): continue
            future = self.getBox(frame=frame, boundary=False)
            if(future==None): break
            error = getError(history, future)
            if(error>96): break
            delta = time
            continue
        tail = int(interval[0] + delta) if(delta!=None) else int(interval[0])
        # if(delta==None): tail = int(interval[0])
        # else: tail = int(interval[0]+delta)
        return(tail)

    pass

def saveDetection(path):
    folder = os.path.dirname(path)
    mark = os.path.join(folder, 'detection')
    status = os.path.isfile(mark)
    if(status): 
        print(f"Detect [{path}] already.")
        return
    print(f"Start to detect [{path}].")
    video = moviepy.editor.VideoFileClip(path).set_fps(25)
    length = int(video.duration*0.5)
    video = video.subclip(0, length)
    interval = [0, length]
    agent = Agent()
    agent.makeModel()
    detection = []
    while(True):
        if(interval[0]>=length):break
        head = agent.getHead(video, interval)
        if(head<0): break
        interval = [head, length]
        tail = agent.getTail(video, interval)
        if(tail-head<1):
            interval = [tail+1, length]
            continue
        frame = video.subclip(head, tail).get_frame(0.0)
        box = agent.getBox(frame, boundary=True)
        if(box==None):
            interval = [tail+1, length]
            continue
        item = [head, tail, box]
        detection += [item]
        interval = [tail+1, length]
        continue
    for index, item in enumerate(detection):
        head, tail, box = item
        title = os.path.basename(folder)
        name = "_".join([title, str(head), str(tail), str(index)])
        scope = video.subclip(head, tail)
        fragment = scope.crop(box[0], box[1], box[2], box[3])
        fragment.write_videofile(
            f'{folder}/{name}.mp4', 
            codec="libx264", 
            logger=None, 
            temp_audiofile=f'{folder}/{name}.wav'
        )
        shot = PIL.Image.fromarray(fragment.get_frame(0.0))
        shot.save(f'{folder}/{name}.jpg')
        continue
    del agent
    pathlib.Path(mark).touch()
    print(f'Save detection to [{folder}].')
    return

class Extraction:

    def __init__(self, folder, core):
        self.folder = folder
        self.core = core
        return

    def saveDetection(self):
        iteration = glob.glob(os.path.join(self.folder, '*/video.mp4'))
        pool = multiprocessing.Pool(self.core)
        _ = pool.map(saveDetection, iteration)
        return

    pass

if(__name__=='__main__'):
    definition = argparse.ArgumentParser()
    definition.add_argument("--folder", default='2023壹電視新聞10-12-B', type=str)
    definition.add_argument("--core", default=8, type=int)
    argument = definition.parse_args()
    extraction = Extraction(argument.folder, argument.core)
    extraction.saveDetection()
    pass

