import os
import glob
import moviepy.editor
import tqdm
import argparse
import multiprocessing
def savePeriod(path):
    # path = '【數位主播午報】/1x3g0XJ50Fg/1x3g0XJ50Fg_0_31.mp4'
    name = os.path.basename(path).replace(".mp4", '')
    folder = os.path.join(
        os.path.dirname(path),
        name
    )
    video = moviepy.editor.VideoFileClip(path)
    length = int(video.duration)
    threshold = 1
    if(length<threshold): return
    os.makedirs(folder, exist_ok=True)
    for index in range(length):
        period = video.subclip(index, index+1)
        number = len([i for i in period.iter_frames()])
        if(number!=threshold*25): continue
        if(os.path.isfile(f'{folder}/{name}_{index}.mp4')): continue
        period.write_videofile(
            f'{folder}/{name}_{index}.mp4', 
            codec="libx264", 
            logger=None, 
            temp_audiofile=f'{folder}/{name}_{index}.wav'
        )
        continue
    return    

if(__name__=='__main__'):
    definition = argparse.ArgumentParser()
    definition.add_argument("--folder", default='壹電視新聞-2023(7-9月)/C', type=str)
    argument = definition.parse_args()
    # folder = './【數位主播午報】'
    element = glob.glob(os.path.join(argument.folder, '*/*.mp4'))
    element = [e for e in element if('video' not in e)]
    core = 6
    pool = multiprocessing.Pool(core)
    _ = pool.map(savePeriod, element)
    # for path in tqdm.tqdm(element):
    #     savePeriod(path)
    #     continue