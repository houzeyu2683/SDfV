import logging
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

def getBox(frame, boundary):
    experiment = tensorflow.config.experimental
    for item in experiment.list_physical_devices('GPU'):
        experiment.set_memory_growth(item, True)
        _ = experiment.list_logical_devices('GPU')
        continue
    height, width, _ = frame.shape
    response = retinaface.RetinaFace.detect_faces(frame)
    if(len(response)!=1): return 
    area = response['face_1']['facial_area']
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

def getError(history, future):
    comparison = numpy.array(history) - numpy.array(future)
    error = numpy.absolute(comparison).sum()
    return(error)

class Extraction:

    def __init__(self, path):
        self.path = path
        return

    def getVideo(self):
        video = moviepy.editor.VideoFileClip(self.path).set_fps(25)
        length = int(video.duration)
        video = video.subclip(0, length)
        return(video)

    def getLength(self):
        video = self.getVideo()
        length = video.duration
        return(length)

    def getHead(self, interval):
        delta = None
        video = self.getVideo()
        video = video.subclip(interval[0], interval[1])
        progress = video.iter_frames(with_times=True)
        for index, (time, frame) in enumerate(progress):
            if(index % 25!=0): continue
            box = getBox(frame=frame, boundary=False)
            if(box==None): continue
            delta = time
            break
        head = int(interval[0] + delta) if(delta!=None) else delta
        return(head)

    def getTail(self, interval):
        delta = None
        head = self.getHead(interval)
        if(head==None): 
            tail = delta
            return(tail)
        video = self.getVideo()
        video = video.subclip(head, interval[1])
        progress = video.iter_frames(with_times=True)
        for index, (time, frame) in enumerate(progress):
            if(index==0):
                history = getBox(frame=frame, boundary=False)
                if(history==None): 
                    tail = int(head)
                    return(tail)
                continue
            if(index % 4!=0): continue
            future = getBox(frame=frame, boundary=False)
            if(future==None): break
            error = getError(history, future)
            if(error>96): break
            delta = time
            continue        
        tail = int(head+delta) if(delta!=None) else delta
        return(tail)

    def makeDetection(self):
        length = self.getLength()
        interval = [0, length]
        detection = []
        print(f'Start to detect [{self.path}] file.')
        while(True):
            head = self.getHead(interval)
            tail = self.getTail(interval)
            if(head==None or tail==None): break
            if((tail - head)<1):
                interval = [tail+1, length]
                continue
            frame = self.getVideo().subclip(head, tail).get_frame(0.0)
            box = getBox(frame=frame, boundary=True)
            if(box==None):
                interval = [tail+1, length]
                continue
            folder = os.path.dirname(self.path)
            tag = os.path.basename(folder)
            name = '_'.join([tag, str(head), str(tail)])
            item = {
                'head': head, 
                'tail': tail, 
                'box':box, 
                'folder': folder,
                'name': name
            }
            detection += [item]
            if((tail+1)>=length): break
            interval = [tail+1, length]
            continue
        print(f'Finish to detect [{self.path}] file.')
        self.detection = detection
        return

    def saveDetection(self):
        print(f'Start to save [{self.path}] detection.')
        video = self.getVideo()
        for detection in self.detection:
            head, tail = detection['head'], detection['tail']
            box = detection['box']
            folder = detection['folder']
            name = detection['name']
            moment = video.subclip(head, tail)
            moment = moment.crop(box[0], box[1], box[2], box[3])
            moment.write_videofile(
                f'{folder}/{name}.mp4', 
                codec="libx264", 
                logger=None, 
                temp_audiofile=f'{folder}/{name}.wav'
            )
            continue
        folder = os.path.dirname(self.path)
        pathlib.Path(os.path.join(folder, 'detection')).touch()
        print(f'Finish to save [{self.path}] detection.')
        return

    pass

if(__name__=='__main__'):
    definition = argparse.ArgumentParser()
    definition.add_argument("--folder", default='壹電視新聞-2023(7-9月)', type=str)
    argument = definition.parse_args()
    folder = argument.folder
    print(f'Start to capture [{folder}] folder.')
    loop = glob.glob(os.path.join(folder, '*/video.mp4'))
    for path in loop:
        mark = os.path.join(os.path.dirname(path), 'detection')
        if(os.path.isfile(mark)): continue
        extraction = Extraction(path)
        extraction.makeDetection()
        extraction.saveDetection()
        continue
    print(f'Finish to capture [{folder}] folder.')
    pass





