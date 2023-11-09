import glob
import os
import shutil

loop = [
    '數位主播/午報/',
    '數位主播/晚報/',
    '主播焦點新聞/0001-0600/',
    '主播焦點新聞/0601-1200/'
]
folder = 'source/'
os.makedirs(folder, exist_ok=True)
for batch in loop:
    iteration = glob.glob(f'{batch}/*/positive/*.mp4')
    for item in iteration:
        unit = item.split('positive')[0].split(batch)[-1].replace('/', "")
        index = os.path.basename(item)
        path = os.path.join(folder, unit, index)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        shutil.copy(item, path)
        continue
    continue