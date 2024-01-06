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

class Agent:

    def __init__(self):
        return

    def getHead(self, video, interval):
        delta = None
        video = video.subclip(interval[0], interval[1])
        progress = video.iter_frames(with_times=True)
        for index, (time, frame) in enumerate(progress):
            if(index % 25!=0): continue
            box = getBox(frame=frame, boundary=False)
            if(box==None): continue
            delta = time
            break
        head = int(interval[0] + delta) if(delta) else -1        
        return(head)

    def getTail(self, video, interval):
        delta = None
        video = video.subclip(interval[0], interval[1])
        progress = video.iter_frames(with_times=True)
        for index, (time, frame) in enumerate(progress):
            if(index==0):
                history = getBox(frame=frame, boundary=False)
                if(history==None): 
                    tail = int(interval[0])
                    return(tail)
                continue
            if(index % 4!=0): continue
            future = getBox(frame=frame, boundary=False)
            if(future==None): break
            error = getError(history, future)
            if(error>96): break
            delta = time
            continue
        tail = int(interval[0] + delta) if(delta) else int(interval[0])
        # if(delta==None): tail = int(interval[0])
        # else: tail = int(interval[0]+delta)
        return(tail)

    pass

def saveDetection(path):
    folder = os.path.dirname(path)
    mark = os.path.join(folder, 'detection')
    status = os.path.isfile(mark)
    if(status): return
    video = moviepy.editor.VideoFileClip(path).set_fps(25)
    length = int(video.duration*0.5)
    video = video.subclip(0, length)
    interval = [0, length]
    agent = Agent()
    detection = []
    while(True):
        if(interval[0]>=length):break
        head = agent.getHead(video, interval)
        if(head<1): break
        interval = [head, length]
        tail = agent.getTail(video, interval)
        if(tail-head<1):
            interval = [tail+1, length]
            continue
        frame = video.subclip(head, tail).get_frame(0.0)
        box = getBox(frame, boundary=True)
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
    return(detection)

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
    definition.add_argument("--folder", default='sample', type=str)
    # definition.add_argument("--core", default=8, type=int)
    argument = definition.parse_args()
    # print(f'Start to capture [{argument.folder}] folder.')
    extraction = Extraction(argument.folder, 1)
    extraction.saveDetection()
    pass

# def getBox(frame, boundary, method):
#     if(method==0):
#         experiment = tensorflow.config.experimental
#         for item in experiment.list_physical_devices('GPU'):
#             experiment.set_memory_growth(item, True)
#             _ = experiment.list_logical_devices('GPU')
#             continue
#         height, width, _ = frame.shape
#         response = retinaface.RetinaFace.detect_faces(frame)
#         if(len(response)!=1): return 
#         area = response['face_1']['facial_area']
#         point = response['face_1']["landmarks"]
#         x = numpy.array(point["left_eye"]) - numpy.array(point['nose'])
#         y = numpy.array(point["right_eye"]) - numpy.array(point['nose'])
#         angle = getAngle(x, y)
#         if(angle<60 or angle>100): return
#         pass
#     if(method==1):
#         device = 'cuda' if(torch.cuda.is_available()) else 'cpu'
#         model = facenet_pytorch.MTCNN(
#             keep_all=True, 
#             device=device, 
#             post_process=False
#         )
#         height, width, _ = frame.shape
#         area, confidence = model.detect(frame)
#         if(confidence[0]==None or len(confidence)>1): return
#         area = area.astype(int).flatten().tolist()
#         pass
#     if(boundary):
#         scale = 1.0
#         box = [
#             max(0, area[0]-int((area[2]- area[0])*scale)),
#             max(0, area[1]-int((area[3]- area[1])*scale)),
#             min(width, area[2]+int((area[2]- area[0])*scale)),
#             min(height, area[3]+int((area[3]- area[1])*scale))
#         ]
#         pass
#     else: box = area
#     return(box)



# class Fragment:

#     def __init__(self, path):
#         self.path = path
#         return

#     def getVideo(self):
#         video = moviepy.editor.VideoFileClip(self.path).set_fps(25)
#         length = int(video.duration)
#         video = video.subclip(0, length)
#         return(video)

#     def getLength(self):
#         video = self.getVideo()
#         length = video.duration
#         return(length)

#     def getHead(self, interval):
#         delta = None
#         video = self.getVideo()
#         video = video.subclip(interval[0], interval[1])
#         progress = video.iter_frames(with_times=True)
#         for index, (time, frame) in enumerate(progress):
#             if(index % 25!=0): continue
#             box = getBox(frame=frame, boundary=False, method=0)
#             if(box==None): continue
#             delta = time
#             break
#         head = int(interval[0] + delta) if(delta!=None) else delta
#         return(head)

#     def getTail(self, interval):
#         delta = None
#         head = self.getHead(interval)
#         if(head==None): 
#             tail = delta
#             return(tail)
#         video = self.getVideo()
#         video = video.subclip(head, interval[1])
#         progress = video.iter_frames(with_times=True)
#         for index, (time, frame) in enumerate(progress):
#             if(index==0):
#                 history = getBox(frame=frame, boundary=False, method=0)
#                 if(history==None): 
#                     tail = int(head)
#                     return(tail)
#                 continue
#             if(index % 4!=0): continue
#             future = getBox(frame=frame, boundary=False, method=0)
#             if(future==None): break
#             error = getError(history, future)
#             if(error>96): break
#             delta = time
#             continue        
#         tail = int(head+delta) if(delta!=None) else delta
#         return(tail)

#     def makeDetection(self):
#         length = self.getLength()
#         interval = [0, length]
#         detection = []
#         # print(f'Start to detect [{self.path}] file.')
#         while(True):
#             head = self.getHead(interval)
#             tail = self.getTail(interval)
#             if(head==None or tail==None): break
#             if(head>(length*0.6)): break
#             if((tail - head)<1):
#                 interval = [tail+1, length]
#                 continue
#             frame = self.getVideo().subclip(head, tail).get_frame(0.0)
#             box = getBox(frame=frame, boundary=True, method=0)
#             if(box==None):
#                 interval = [tail+1, length]
#                 continue
#             # folder = os.path.dirname(self.path)
#             tag = os.path.basename(os.path.dirname(self.path))
#             name = '_'.join([tag, str(head), str(tail)])
#             item = {
#                 'head': head, 
#                 'tail': tail, 
#                 'box':box, 
#                 # 'folder': folder,
#                 'name': name
#             }
#             detection += [item]
#             if((tail+1)>=length): break
#             interval = [tail+1, length]
#             continue
#         print(f'Finish to detect [{self.path}] file.')
#         self.detection = detection
#         return

#     def saveDetection(self):
#         # print(f'Start to save [{self.path}] detection.')
#         folder = os.path.dirname(self.path)
#         video = self.getVideo()
#         for detection in self.detection:
#             head, tail = detection['head'], detection['tail']
#             box = detection['box']
#             # folder = detection['folder']
#             name = detection['name']
#             moment = video.subclip(head, tail)
#             moment = moment.crop(box[0], box[1], box[2], box[3])
#             moment.write_videofile(
#                 f'{folder}/{name}.mp4', 
#                 codec="libx264", 
#                 logger=None, 
#                 temp_audiofile=f'{folder}/{name}.wav'
#             )
#             shot = PIL.Image.fromarray(moment.get_frame(0.0))
#             shot.save(f'{folder}/{name}.jpg')
#             continue
#         mark = os.path.join(folder, 'detection')
#         pathlib.Path(mark).touch()
#         print(f'Finish to save [{self.path}] detection.')
#         return

#     def getStatus(self):
#         folder = os.path.dirname(self.path)
#         mark = os.path.join(folder, 'detection')
#         status = True if(os.path.isfile(mark)) else False
#         return(status)

#     pass

# class Extraction:

#     def __init__(self, folder):
#         self.folder = folder
#         return
    
#     def makeMoment(self):
#         path = os.path.join(self.folder, '*/video.mp4')
#         moment = glob.glob(path)
#         self.moment = moment
#         return

#     def saveMoment(self, core=8):
#         pool = multiprocessing.Pool(core)
#         _ = pool.map(saveMoment, self.moment)
#         return

#     pass

# def saveMoment(path):
#     fragment = Fragment(path)
#     status = fragment.getStatus()
#     if(status): 
#         print(f'Finish [{path}] already.')
#         return
#     fragment.makeDetection()
#     fragment.saveDetection()
#     return







