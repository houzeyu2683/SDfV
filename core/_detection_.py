import os
import moviepy.editor
import face_recognition
import time
import PIL.Image
import math 
import multiprocessing
import functools
import tqdm

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
    print(f'Read {path} and make fragment.')
    video = moviepy.editor.VideoFileClip(path)
    width, height = video.size
    length = int(video.duration)
    for moment in range(length):
        if(moment<(length*head) or moment>(length*tail)): continue
        second = [moment, moment+1]
        image = [video.get_frame(second[0]), video.get_frame(second[1])]
        face = [getFace(i) for i in image]
        box = [face[0][0], face[1][0]]
        status = [face[0][1], face[1][1]]
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
    os.remove(path)
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
    
    def makeFragment(self, thread=1):
        iteration = self.getIteration()
        if(thread<=1):
            for item in tqdm.tqdm(iteration, leave=False):
                makeFragment(path=item, head=self.head, tail=self.tail)
                continue
            pass
        else:
            process = multiprocessing.Pool(processes=thread)
            function = functools.partial(makeFragment, head=self.head, tail=self.tail)
            _ = process.map(function, iteration)
            process.close()
            pass
        return
    
    pass
