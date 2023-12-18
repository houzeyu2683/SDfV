import selenium.webdriver
import time
import multiprocessing
import shutil
import yt_dlp
import functools
import argparse
import os

class Channel:

    def __init__(self):
        return

    def getInventory(self, path):
        iteration = None
        here = os.path.exists(path)
        if(here):
            record = open(path, 'r')
            iteration = [_.replace("\n", "") for _ in record.readlines()]
            record.close()
            pass
        inventory = iteration 
        return(inventory)

    def makeInventory(self, link, display):
        option = selenium.webdriver.ChromeOptions()
        if(not display): option.add_argument("--headless")
        driver = selenium.webdriver.Chrome(options=option)
        driver.get(link)
        time.sleep(1)
        script = 'document.documentElement.scrollHeight'
        height = driver.execute_script(f"return {script}")
        while True:
            command = f"window.scrollTo(0, {script});"
            driver.execute_script(command)
            time.sleep(0.5)
            update = driver.execute_script(f"return {script}")
            if(height==update):break
            else: height=update
            continue
        iteration = []
        for item in driver.find_elements('id', "video-title"):
            content = item.get_attribute('href')
            head = 'https://www.youtube.com/watch?v='
            body = content.split('?v=')[-1].split('&')[0]
            if(content): iteration += [f'{head}{body}']
            continue
        driver.close()
        self.inventory = iteration
        return

    def saveInventory(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        record = open(f"{path}", 'w')
        for item in self.inventory: record.write(f"{item}\n")
        record.close()
        return

    pass

def saveVideo(link, folder):
    os.makedirs(os.path.dirname(folder), exist_ok=True)
    identity = link.split('?')[-1].split('=')[-1].split("&")[0]
    path = os.path.join(folder, identity, 'video.mp4')
    finish = os.path.isfile(path)
    if(finish): return
    shutil.rmtree(os.path.dirname(path), ignore_errors=True)
    option = {
        'quiet': True,
        'verbose': False,
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=mp4]/mp4',
        "outtmpl": f'{path}'
    }
    process = yt_dlp.YoutubeDL(option)
    try:_ = process.download(link)
    except: shutil.rmtree(os.path.dirname(path), ignore_errors=True)
    process.close()    
    return

class Media:

    def __init__(self):
        return
    
    def saveVideo(self, inventory, core, folder):
        pool = multiprocessing.Pool(processes=core)
        function = functools.partial(
            saveVideo, 
            folder = folder

        )
        _ = pool.map(function, inventory)
        pool.close()
        return

    pass

if(__name__=='__main__'):
    definition = argparse.ArgumentParser()
    definition.add_argument("--link", default=None, type=str)
    definition.add_argument("--folder", default=None, type=str)
    definition.add_argument("--core", default=4, type=int)
    argument = definition.parse_args()
    link = argument.link
    folder = argument.folder
    core = argument.core
    #
    tag = link.split('=')[-1]
    channel = Channel()
    channel.makeInventory(link=link, display=False)
    channel.saveInventory(path=)
    inventory = channel.getInventory(path)
    media = Media()
    media.saveVideo(inventory, core=core, folder=folder)
    pass
