import selenium.webdriver
import time
import os
import multiprocessing
import shutil
import tqdm
import yt_dlp
import functools
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

class Batch:

    def __init__(self):
        return
    
    def makeGroup(self, folder):
        element = []
        for item in folder:
            section = os.path.join(item, "*/*.mp4")
            element += glob.glob(section)
            continue
        group = [e for e in element if('video.mp4' not in e)]
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
        print(f"Save in the [{folder}].")
        return

    pass


if(__name__=='__main__'):
    definition = argparse.ArgumentParser()
    definition.add_argument("--folder", default='', type=str)
    argument = definition.parse_args()
    folder = argument.folder.split("&")
    batch = Batch()
    batch.makeGroup(folder)
    batch.saveGroup()
    pass