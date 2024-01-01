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
        self.detection = detection
        return

    def saveDetection(self):
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
        pathlib.Path(f'{folder}/detection').touch()
        return

    pass

extraction = Extraction(path='./sample/pFegkQJYOGc/video.mp4')
extraction.makeDetection()

# interval = [0, extraction.getLength()]
# extraction.getHead(interval)
# extraction.getTail(interval)

#     def getDetection(self, scope):
#         video = self.getVideo().subclip(scope[0], scope[1])
#         bound, _ = scope
#         head, tail = None, None
#         progress = video.iter_frames(with_times=True)
#         for index, (time, frame) in enumerate(progress):
#             if(index % 4!=0): continue
#             box = getBox(frame=frame, boundary=False)
#             if(box==None): continue
#             head = time
#             break
#         if(head==None): 
#             detection = None
#             return(detection)
#         progress = video.iter_frames(with_times=True)
#         for index, (time, frame) in enumerate(progress):
#             if(index % 4!=0): continue
#             if(time<head): continue
#             if(time==head): 
#                 history = getBox(frame=frame, boundary=False)
#                 continue
#             future = getBox(frame=frame, boundary=False)
#             if(future==None):
#                 scope = [int(time+bound+1), self.getLength()]
#                 break
#             error = getError(history, future)
#             if(error>96): 
#                 scope = [int(time+bound+1), self.getLength()]
#                 break
#             tail = time
#             continue
#         if(tail==None): 
#             detection = None
#             return(detection)
#         frame = video.subclip(head, tail).get_frame(0.0)
#         box = getBox(frame=frame, boundary=True)
#         if(box==None): 
#             code = [int(bound+head+1)] + [int(bound+tail)]
#             pass
#         else: 
#             code = [int(bound+head+1)] + [int(bound+tail)] + box
#             pass
#         folder = video.filename.replace('video.mp4', '')
#         name = os.path.basename(os.path.dirname(video.filename))
#         tag = '_'.join([str(x) for x in code])
#         path = os.path.join(folder, f'{name}_{tag}.mp4')
#         detection = {
#             "head": bound+head,
#             "tail": bound+tail,
#             'scope': scope, 
#             'box': box, 
#             'path':path
#         }
#         return(detection)
    
#     def makeFragment(self):
#         print(f'Load video from [{self.path}].')
#         fragment = []
#         scope = [0, self.getLength()]
#         while(True):
#             detection = self.getDetection(scope)
#             if(detection==None): break
#             scope = detection['scope']
#             length = int(detection['tail']) - int(detection['head']+1)
#             box = detection['box']
#             if(length<1 or box==None): continue
#             head = round(detection['head'], 2)
#             tail = round(detection['tail'], 2)
#             print(f"Make fragment from {head} to {tail} second.")
#             fragment += [detection]
#             continue
#         self.fragment = fragment
#         return

#     def saveFragment(self):
#         for detection in self.fragment:
#             head = int(detection['head']+1)
#             tail = int(detection['tail'])
#             box = detection['box']
#             path = detection['path']
#             # video = self.getVideo().subclip(head, tail)
#             video = detection['video']
#             video = video.subclip(head, tail)
#             video = video.crop(box[0], box[1], box[2], box[3])
#             if(os.path.isfile(path)):return
#             os.makedirs(os.path.dirname(path), exist_ok=True)
#             video.write_videofile(
#                 path, 
#                 codec="libx264", 
#                 logger=None, 
#                 temp_audiofile=path.replace(".mp4", '.wav')
#             )            
#             print(f"Save fragment to [{path}].")
#             continue
#         print(f"Finish fragment from [{self.path}].")
#         return

#     pass

# if(__name__=='__main__'):
#     definition = argparse.ArgumentParser()
#     definition.add_argument("--folder", default='./sample/', type=str)
#     argument = definition.parse_args()
#     loop = glob.glob(os.path.join(argument.folder, '*/video.mp4'))
#     for path in loop:
#         extraction = Extraction(path=path)
#         extraction.makeFragment()
#         extraction.saveFragment()
#         continue
#     pathlib.Path(os.path.join(argument.folder, 'Extraction')).touch()
#     pass


# # path = './sample/pFegkQJYOGc/video.mp4'
# # extraction = Extraction(path)
# # extraction.makeFragment()

