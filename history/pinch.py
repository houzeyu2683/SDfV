import glob
import os
import moviepy.editor
import tqdm
import pathlib
import multiprocessing
import argparse


class Media:

    def __init__(self):
        return
    
    def saveMoment(self, folder, core):
        iteration = glob.glob(os.path.join(folder, '*/'), recursive=True)
        pool = multiprocessing.Pool(core)
        pool.map(saveMoment, iteration)
        return

    pass

def saveMoment(folder):
    mark = os.path.join(folder, 'moment.txt')
    if(os.path.isfile(mark)): return
    path = os.path.join(folder, 'video.mp4')
    video = moviepy.editor.VideoFileClip(path).set_fps(25)
    schedule = tqdm.tqdm(glob.glob(os.path.join(folder, '*.jpg')))
    for item in schedule:
        schedule.set_description(f"Process [{item}] file.")
        shot = item.replace(".jpg", "")
        index = int(shot.split("_")[-5])
        area = shot.split("_")[-4:]
        boundary = [int(_) for _ in area]
        moment = video.subclip(index, index+1).crop(
            boundary[0],
            boundary[1],
            boundary[2],
            boundary[3]
        )
        moment.write_videofile(
            f'{shot}.mp4', 
            codec="libx264", 
            logger=None, 
            temp_audiofile=f'{shot}_temp_audio.wav'
        )
        continue
    message = pathlib.Path(mark)
    _ = message.write_text(f'Make moment successfully.')    
    return

if(__name__=='__main__'):
    definition = argparse.ArgumentParser()
    definition.add_argument("--folder", default='./PLiY6wtxjK6QObLNvU8fwx6XYXFYwYWww-/', type=str)
    definition.add_argument("--core", default=4, type=int)
    argument = definition.parse_args()
    media = Media()
    media.saveMoment(argument.folder, argument.core)
    pass

# folder = 'PLiY6wtxjK6QObLNvU8fwx6XYXFYwYWww-/'
# media = Media()
# media.saveMoment(folder=folder, core=2)