import logging
import os
import glob
import moviepy.editor
import retinaface.RetinaFace
import tensorflow
import numpy
import multiprocessing

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

class Fragment:

    def __init__(self, path):
        self.path = path
        return

    def makeVideo(self):
        video = moviepy.editor.VideoFileClip(self.path).set_fps(25)
        length = int(video.duration)
        self.video = video.subclip(0, length)
        return

    def getLength(self):
        length = int(self.video.duration)
        return(length)

    def makeDetection(self, scope):
        length = self.getLength()
        head, tail = None, None
        for time, frame in self.video.iter_frames(with_times=True):
            if(not (scope[0]<=time<=scope[1])): continue
            box = getBox(frame=frame, boundary=False)
            if(box==None): continue
            head = time
            break
        for time, frame in self.video.iter_frames(with_times=True):
            if(time<head): continue
            if(time==head): 
                history = getBox(frame=frame, boundary=False)
                continue
            future = getBox(frame=frame, boundary=False)
            if(future==None):
                scope = [time, length]
                break
            comparison = [h-f for h, f in zip(history, future)]
            error = numpy.array(comparison).sum()
            if(error>96): 
                scope = [time, length]
                break
            tail = time
            continue
        if(head==None or tail==None): 
            detection = None
            self.detection = detection
            return
        print(f"Capture detection from {head} to {tail} time.")
        frame = self.video.subclip(head, tail).get_frame(0.0)
        box = getBox(frame=frame, boundary=True)
        folder = self.video.filename.replace('video.mp4', '')
        name = os.path.basename(os.path.dirname(self.video.filename))
        if(box==None): 
            code = [int(head+1)] + [int(tail)] + [0,0,0,0]
            pass
        else: 
            code = [int(head+1)] + [int(tail)] + box
            pass
        tag = '_'.join([str(x) for x in code])
        path = os.path.join(folder, f'{name}_{tag}.mp4')
        detection = {
            "head": head,
            "tail": tail,
            'scope': scope, 
            'box': box, 
            'path':path
        }
        self.detection = detection
        return
    
    def saveDetection(self):
        head, tail = self.detection['head'], self.detection['tail']
        if((tail-head)<1): return
        if((tail-head)>3): head, tail = int(head+1), int(tail)
        box = self.detection['box']
        if(box==None): return
        video = self.video.subclip(head, tail)
        video = video.crop(box[0], box[1], box[2], box[3])
        path = self.detection['path']
        if(os.path.isfile(path)):return
        os.makedirs(os.path.dirname(path), exist_ok=True)
        video.write_videofile(
            path, 
            codec="libx264", 
            logger=None, 
            temp_audiofile=path.replace(".mp4", '.wav')
        )
        return

    pass

def saveExtraction(path):
    fragment = Fragment(path)
    fragment.makeVideo()
    length = fragment.getLength()
    scope = [0, length]
    while(True):
        fragment.makeDetection(scope)
        if(fragment.detection==None): break
        scope = fragment.detection['scope']
        fragment.saveDetection()
        continue
    print(f"Save [{path}]'s extraction.")
    return

# folder = './sample/'
# loop = glob.glob(os.path.join(folder, '*/video.mp4'))
# for item in loop:
#     saveExtraction(item)
#     continue
# core = 6
# pool = multiprocessing.Pool(core)
# pool.map(saveExtraction, loop)
path = './sample/mF1aMad426U/video.mp4'
saveExtraction(path)