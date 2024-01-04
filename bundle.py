import os
import shutil
import tqdm
import argparse
import sklearn.model_selection
import glob

def writeFile(content, path):
    with open(path, 'w') as paper:
        for item in content:
            paper.write("%s\n" % item)
            continue
        pass
    return

def getElement(folder):
    wall = glob.glob(os.path.join(folder, "*/*.mp4"))
    iteration = os.walk(folder, topdown=False)
    element = []
    for root, leaf, node in iteration:
        for name in node:
            item = os.path.join(root, name)
            if('mp4' not in item): continue
            if('video.mp4' in item): continue
            if('skip' in item): continue
            if(item in wall): continue          
            # target = ('.mp4' in item)
            # if(target): element += [item]
            element += [item]
            continue
        _ = leaf
        continue
    return(element)

class Batch:

    def __init__(self):
        return
    
    def makeGroup(self, folder):
        group = []
        for item in folder:
            group += getElement(item)
            continue
        self.group = group
        return

    def saveGroup(self):
        folder = "group"
        length = len(self.group)
        for path in tqdm.tqdm(self.group, total=length, leave=False):
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
    definition.add_argument("--folder", default='【數位主播午報】&【數位主播晚報】&壹電視新聞-2023(7-9月)/A&壹電視新聞-2023(7-9月)/B&壹電視新聞-2023(7-9月)/C', type=str)
    argument = definition.parse_args()
    folder = argument.folder.split("&")
    batch = Batch()
    batch.makeGroup(folder)
    batch.saveGroup()
    pass

