import os
import moviepy.editor
import time
import PIL.Image
import math 
import multiprocessing
import functools
import dlib
import tqdm
import face_recognition
import pathlib

def getFace(image):
    prediction = face_recognition.face_locations(image)
    if(len(prediction)!=1):
        box, status = None, False
        pass
    else:
        box, status = prediction[0], True
        top, right, bottom, left = box
        box = left, top, right, bottom
        pass
    face = box, status
    return(face)


def makeFragment(path, head=0, tail=1):
    invoice = path.replace('video.mp4', 'fragment.txt')
    if(os.path.isfile(invoice)): return
    print(f'Make {path} fragment.')
    video = moviepy.editor.VideoFileClip(path)
    width, height = video.size
    length = int(video.duration)
    loop = enumerate(range(length), start=1)
    progress = tqdm.tqdm(loop, total=length)
    for _, moment in progress:
        # print(f"|{number}/{length}|")
        if(moment<(length*head) or moment>(length*tail)): continue
        second = [moment, moment+1]
        image = [video.get_frame(i) for i in second]
        recognition = [getFace(i) for i in image]
        box = [recognition[0][0], recognition[1][0]]
        status = [recognition[0][1], recognition[1][1]]
        if(sum(status)!=2): continue
        lock = video.subclip(second[0], second[1])
        limit = max(box[0][2] - box[0][0], box[0][3] - box[0][1])
        area = (box[0][2] - box[0][0]) * (box[0][3] - box[0][1])
        center = []
        for b in box:
            c = [(b[0]+b[2])/2, (b[1]+b[3])/2]
            center += [c]
            continue
        delta = []
        delta += [abs(center[0][0] - center[1][0])]
        delta += [abs(center[0][1] - center[1][1])]
        delta = sum(delta)
        if(area<=96*96 or delta>math.sqrt(area)): continue 
        fragment = lock.crop(
            x1=max(0, box[0][0]-limit),
            y1=max(0, box[0][1]-limit),
            x2=min(width, box[0][2]+limit),
            y2=min(height, box[0][3]+limit)
        )
        shot = PIL.Image.fromarray(fragment.get_frame(0))
        time.sleep(1)
        tag = f'{os.path.dirname(path)}/{moment}'
        fragment.write_videofile(
            f'{tag}.mp4', 
            codec="libx264", 
            logger=None, 
            temp_audiofile=f'{tag}.wav'
        )
        shot.save(f'{tag}.jpg')
        continue
    time.sleep(1)
    video.close()
    pathlib.Path(invoice).touch()
    return

class Detection:

    def __init__(self, folder, head, tail):
        self.folder = folder
        self.head = head
        self.tail = tail
        return    
    
    def getIteration(self):
        iteration = []
        for tag in os.listdir(self.folder):
            item = os.path.join(self.folder, tag, 'video.mp4')
            here = os.path.isfile(item)
            if(not here): continue
            iteration += [item]
            continue
        return(iteration)
    
    def makeFragment(self):
        iteration = self.getIteration()
        length = len(iteration)
        # loop = enumerate(iteration, start=1)
        # progress = tqdm.tqdm(loop, total=length, leave=False)
        for number, item in enumerate(iteration, start=1):
            print(f"|{number}/{length}|")
            # progress.set_description(f"|{number}/{length}|")
            makeFragment(path=item, head=self.head, tail=self.tail)
            continue
        return
    
    pass
