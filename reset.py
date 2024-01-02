import os
import shutil
import glob

folder = './【數位主播晚報】'
for path in glob.glob(os.path.join(folder, "*/*")):
    if('video.mp4'in path): continue
    if(os.path.isdir(path)):
        shutil.rmtree(path)
        continue
    os.remove(path)
    continue

