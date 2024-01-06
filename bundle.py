import os
import shutil
import tqdm
import argparse
import sklearn.model_selection
import glob
import moviepy.editor

def writeFile(content, path):
    with open(path, 'w') as paper:
        for item in content:
            paper.write("%s\n" % item)
            continue
        pass
    return

def getElement(folder):
    # wall = glob.glob(os.path.join(folder, "*/*.mp4"))
    # iteration = os.walk(folder, topdown=False)
    loop = glob.glob(os.path.join(folder, '*/*'))
    element = []
    for path in loop:
        if('video.mp4' in path): continue
        if('detection' in path): continue
        if('skip' in path): continue
        element += [path]
        continue
    return(element)

class Batch:

    def __init__(self):
        return
    
    def makeGroup(self, queue):
        group = []
        for folder in queue:
            group += getElement(folder)
            continue
        self.group = group
        return

    def saveGroup(self):
        folder = "group"
        for path in tqdm.tqdm(self.group, total=len(self.group), leave=False):
            length = int(moviepy.editor.VideoFileClip(path).duration)
            if(length<3): continue
            destination = os.path.join(
                folder,
                os.path.basename(os.path.dirname(path)),
                os.path.basename(path)
            )
            os.makedirs(os.path.dirname(destination), exist_ok=True)
            shutil.copy(path, destination)
            continue
        element = []
        for path in glob.glob(os.path.join(folder, '*/*.mp4')):
            item = os.path.join(
                os.path.basename(os.path.dirname(path)),
                os.path.basename(path).replace(".mp4", '/')
            )
            element += [item]
            continue
        split = sklearn.model_selection.train_test_split
        train, test = split(element, test_size=0.2, random_state=0)
        validation, test = split(test, test_size=0.5, random_state=0)
        writeFile(train, path=os.path.join(folder, 'train.txt'))
        writeFile(validation, path=os.path.join(folder, 'validation.txt'))
        writeFile(test, path=os.path.join(folder, 'test.txt'))
        print(f"Save group in the [{folder}] folder.")
        return

    pass

if(__name__=='__main__'):
    definition = argparse.ArgumentParser()
    definition.add_argument("--folder", default='【數位主播午報】&【數位主播晚報】&壹電視新聞-2023(7-9月)&【年代新聞】2023年7.8.9月', type=str)
    argument = definition.parse_args()
    folder = argument.folder.split("&")
    batch = Batch()
    batch.makeGroup(folder)
    batch.saveGroup()
    pass