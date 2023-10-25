import os
import moviepy.editor
import time
import PIL.Image
import math 
import multiprocessing
import functools
import numpy
# import tqdm
import face_recognition
import pathlib

class Recognition:

    def __init__(self, image):
        self.image = image
        return
    
    def makePrediction(self):
        prediction = face_recognition.face_locations(self.image)
        self.prediction = prediction

    def getStatus(self):
        length = len(self.prediction)
        status = False if(length!=1) else True
        return(status)
    
    def getBox(self):
        length = len(self.prediction)
        box = None
        if(length==1):
            item = self.prediction[0]
            top, right, bottom, left = item
            box = left, top, right, bottom
            pass
        return(box)

    def getCenter(self):
        box = self.getBox()
        center = [(box[0]+box[2])/2, (box[1]+box[3])/2]
        return(center)

    pass

def makeFragment(path, head=0, tail=1):
    invoice = path.replace('video.mp4', 'fragment.txt')
    if(os.path.isfile(invoice)): return
    print(f'Make [{path}] fragment.')
    video = moviepy.editor.VideoFileClip(path)
    width, height = video.size
    length = int(video.duration)
    loop = enumerate(range(length), start=1)
    # progress = tqdm.tqdm(loop, total=length, leave=False)
    for _, moment in loop:
        if(moment<(length*head) or moment>(length*tail)): continue
        one = Recognition(video.get_frame(moment))
        two = Recognition(video.get_frame(moment+1))
        one.makePrediction()
        two.makePrediction()
        if(sum([one.getStatus()+two.getStatus()])!=2): continue
        lock = video.subclip(moment, moment+1)
        box = one.getBox()
        limit = max(box[2] - box[0], box[3] - box[1])
        area = (box[2] - box[0]) * (box[3] - box[1])
        center = numpy.array([one.getCenter(), two.getCenter()])
        delta = abs((center[0,:]-center[1,:])).sum()
        if(area<=96*96 or delta>math.sqrt(area)): continue 
        fragment = lock.crop(
            x1=max(0, box[0]-limit),
            y1=max(0, box[1]-limit),
            x2=min(width, box[2]+limit),
            y2=min(height, box[3]+limit)
        )
        shot = PIL.Image.fromarray(fragment.get_frame(0))
        for item in fragment.iter_frames():
            recognition = Recognition(image=item)
            recognition.makePrediction()
            status = recognition.getStatus()
            if(not status): break
            continue
        if(not status): continue
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
    pathlib.Path(invoice).touch()
    time.sleep(1)
    video.close()
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
            for _, item in enumerate(iteration, start=1):
                makeFragment(path=item, head=self.head, tail=self.tail)
                continue
            pass
        else:
            assert thread<multiprocessing.cpu_count()
            function = functools.partial(
                makeFragment, 
                head=self.head, 
                tail=self.tail
            )
            pool = multiprocessing.Pool(thread)
            pool.map(function, iteration)
            pass
        print('Finish the process for fragment.')
        return
    
    pass
