import os
import glob
import moviepy.editor
import argparse
import multiprocessing
import shutil

def savePeriod(path):
    name = os.path.basename(path).replace(".mp4", '')
    folder = os.path.join(
        os.path.dirname(path),
        name
    )
    if(os.path.isdir(folder)): shutil.rmtree(folder, ignore_errors=True)
    video = moviepy.editor.VideoFileClip(path)
    length = int(video.duration)
    threshold = 2
    if(length<threshold): return
    os.makedirs(folder)
    # for index in range(1):
    period = video#.subclip(index, index+1)
    number = len([i for i in period.iter_frames()])
    # if(number!=threshold*25): continue
    # if(os.path.isfile(f'{folder}/{name}_{index}.mp4')): continue
    period.write_videofile(
        f'{folder}/{name}_{number}.mp4', 
        codec="libx264", 
        logger=None, 
        temp_audiofile=f'{folder}/{name}_{number}.wav'
    )
        # continue
    return    

if(__name__=='__main__'):
    definition = argparse.ArgumentParser()
    definition.add_argument("--folder", default='【數位主播晚報】', type=str)
    argument = definition.parse_args()
    element = glob.glob(os.path.join(argument.folder, '*/*.mp4'))
    element = [e for e in element if('video' not in e)]
    core = 6
    pool = multiprocessing.Pool(core)
    _ = pool.map(savePeriod, element)