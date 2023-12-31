import glob
import os
import moviepy.editor
import retinaface.RetinaFace
import numpy
import PIL.Image
import tqdm
import pathlib
import multiprocessing
import argparse

class Media:

    def __init__(self):
        return
    
    def saveShot(self, folder, core):
        iteration = glob.glob(os.path.join(folder, '*/video.mp4'))
        pool = multiprocessing.Pool(core)
        pool.map(saveShot, iteration)
        return
    
    pass

def saveShot(path):
    folder = os.path.dirname(path)
    mark = os.path.join(folder, 'shot.txt')
    if(os.path.isfile(mark)): return
    tag = os.path.basename(folder)
    video = moviepy.editor.VideoFileClip(path).set_fps(25)
    length = int(video.duration)
    schedule = tqdm.tqdm(range(length))
    for index in schedule:
        schedule.set_description(f"Process [{path}] file.")
        # if(index <= length * 0.1 or index >= length * 0.9): continue
        moment = video.subclip(index, index+1)
        detection = retinaface.RetinaFace.detect_faces(moment.get_frame(0.0))
        if(len(detection)!=1): continue
        box = detection['face_1']['facial_area']
        threshold = min(box[2] - box[0], box[3] - box[1])
        if(threshold<96): continue
        deviation = max(box[2] - box[0], box[3] - box[1])
        width, height = moment.size
        boundary = [
            max(0, box[0]-deviation),
            max(0, box[1]-deviation),
            min(width, box[2]+deviation),
            min(height, box[3]+deviation)
        ]
        pane = moment.crop(
            boundary[0],
            boundary[1],
            boundary[2],
            boundary[3]
        )
        sequence = [
            pane.get_frame(0.00), 
            pane.get_frame(0.25),
            pane.get_frame(0.50), 
            pane.get_frame(0.75),
            pane.get_frame(1.00)
        ]
        shot = PIL.Image.fromarray(numpy.concatenate(sequence, axis=1))
        area = "_".join([str(_) for _ in boundary])
        shot.save(os.path.join(folder, f'{tag}_{index}_{area}.jpg'))
        continue
    message = pathlib.Path(mark)
    _ = message.write_text(f'Make shot successfully.')
    return

if(__name__=='__main__'):
    definition = argparse.ArgumentParser()
    definition.add_argument("--folder", default='./PLiY6wtxjK6QObLNvU8fwx6XYXFYwYWww-/', type=str)
    definition.add_argument("--core", default=4, type=int)
    argument = definition.parse_args()
    media = Media()
    media.saveShot(argument.folder, argument.core)
    pass
