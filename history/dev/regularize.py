import argparse
import os
import moviepy.editor
import PIL.Image
import glob
import tqdm
import retinaface.RetinaFace
import pandas
import multiprocessing
import shutil
import hashlib
import numpy

class Recognition:

    def __init__(self, path):
        self.path = path
        return

    def makeVideo(self):
        video = moviepy.editor.VideoFileClip(self.path)
        video = video.set_fps(25)
        self.video = video
        return

    def getLength(self):
        length = int(self.video.duration)
        return(length)

    def makeDetection(self, index):
        length = self.getLength()
        if(index==length): 
            self.detection = None
            return
        video = self.video.subclip(index, index+1)
        width, height = video.size
        shot = video.get_frame(0.5)
        response = retinaface.RetinaFace.detect_faces(shot)
        if(len(response)!=1): 
            self.detection = None
            return
        area = response['face_1']['facial_area']
        limit = min(area[2] - area[0], area[3] - area[1])
        if(limit<128): 
            self.detection = None
            return
        epsilon = int(limit*0.1)
        box = [
            max(area[0]-epsilon, 0),
            max(area[1]-epsilon, 0),
            min(area[2]+epsilon, width),
            min(area[3]+epsilon, height)
        ]
        detection = video.crop(x1=box[0], y1=box[1], x2=box[2], y2=box[3])
        self.detection = detection
        return

    def makeMoment(self):
        moment = self.detection
        self.moment = moment
        return

    def saveMoment(self, path):
        code = hashlib.sha1(path.encode("utf-8")).hexdigest()
        self.moment.write_videofile(
            path, 
            codec="libx264", 
            audio_codec="aac",
            temp_audiofile=f"{code}.wav",
            logger = None,
        )
        return

    def makeShot(self):
        image = [
            self.moment.get_frame(0.0),
            self.moment.get_frame(0.5),
            self.moment.get_frame(1.0)
        ]
        show = numpy.concatenate(image, axis=1)
        self.show = PIL.Image.fromarray(show)
        return

    def saveShot(self, path):
        self.show.save(path)
        return

    pass

if(__name__=='__main__'):
    definition = argparse.ArgumentParser()
    definition.add_argument("--folder", default='./MOD壹綜合312/', type=str)
    argument = definition.parse_args()
    folder = argument.folder
    #
    for path in tqdm.tqdm(glob.glob(f"{folder}/*/video.mp4"), leave=False):
        recognition = Recognition(path)
        recognition.makeVideo()
        length = recognition.getLength()
        for index in range(length):
            recognition.makeDetection(index)
            if(recognition.detection==None): continue
            recognition.makeMoment()
            tag = os.path.dirname(path)
            recognition.saveMoment(path=f'{tag}_{index}.mp4')
            recognition.makeShot()
            recognition.saveShot(path=f'{tag}_{index}.jpg')
            continue
        continue
    pass