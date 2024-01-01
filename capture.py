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

    def getDetection(self, scope):
        video = self.getVideo()
        length = self.getLength()
        head, tail = None, None
        for time, frame in video.iter_frames(with_times=True):
            if(not (scope[0]<=time<=scope[1])): continue
            box = getBox(frame=frame, boundary=False)
            if(box==None): continue
            head = time
            break
        if(head==None): 
            detection = None
            return(detection)
        for time, frame in video.iter_frames(with_times=True):
            if(time<head): continue
            if(time==head): 
                history = getBox(frame=frame, boundary=False)
                continue
            future = getBox(frame=frame, boundary=False)
            if(future==None):
                scope = [time, length]
                break
            error = getError(history, future)
            if(error>96): 
                scope = [time, length]
                break
            tail = time
            continue
        if(tail==None): 
            detection = None
            return(detection)
        frame = video.subclip(head, tail).get_frame(0.0)
        box = getBox(frame=frame, boundary=True)
        if(box==None): 
            code = [int(head+1)] + [int(tail)]
            pass
        else: 
            code = [int(head+1)] + [int(tail)] + box
            pass
        folder = video.filename.replace('video.mp4', '')
        name = os.path.basename(os.path.dirname(video.filename))
        tag = '_'.join([str(x) for x in code])
        path = os.path.join(folder, f'{name}_{tag}.mp4')
        detection = {
            "head": head,
            "tail": tail,
            'scope': scope, 
            'box': box, 
            'path':path
        }
        return(detection)
    
    def makeFragment(self):
        print(f'Load video from [{self.path}].')
        fragment = []
        scope = [0, self.getLength()]
        while(True):
            detection = self.getDetection(scope)
            if(detection==None): break
            scope = detection['scope']
            length = int(detection['tail']) - int(detection['head']+1)
            box = detection['box']
            if(length<1 or box==None): continue
            head = round(detection['head'], 2)
            tail = round(detection['tail'], 2)
            print(f"Make fragment from {head} to {tail} second.")
            fragment += [detection]
            continue
        self.fragment = fragment
        return

    def saveFragment(self):
        for detection in self.fragment:
            head = int(detection['head']+1)
            tail = int(detection['tail'])
            box = detection['box']
            path = detection['path']
            video = self.getVideo().subclip(head, tail)
            video = video.crop(box[0], box[1], box[2], box[3])
            if(os.path.isfile(path)):return
            os.makedirs(os.path.dirname(path), exist_ok=True)
            video.write_videofile(
                path, 
                codec="libx264", 
                logger=None, 
                temp_audiofile=path.replace(".mp4", '.wav')
            )            
            print(f"Save fragment to [{path}].")
            continue
        print(f"Finish fragment from [{self.path}].")
        return

    pass

if(__name__=='__main__'):
    definition = argparse.ArgumentParser()
    definition.add_argument("--folder", default=None, type=str)
    argument = definition.parse_args()
    loop = glob.glob(os.path.join(argument.folder, '/*/video.mp4'))
    for path in loop:
        extraction = Extraction(path=path)
        extraction.makeFragment()
        extraction.saveFragment()
        continue
    pathlib.Path(os.path.join(argument.folder, 'Extraction')).touch()
    pass


# path = './sample/pFegkQJYOGc/video.mp4'
# extraction = Extraction(path)
# extraction.makeFragment()

