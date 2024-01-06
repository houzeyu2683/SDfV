import selenium.webdriver
import time
import os
import multiprocessing
import shutil
import yt_dlp
import functools
import argparse

def getLink(channel, view):
    part = 'https://www.youtube.com/playlist?list='
    option = selenium.webdriver.ChromeOptions()
    if(not view): option.add_argument("--headless")
    window = selenium.webdriver.Chrome(options=option)
    window.get(f"{part}{channel}")
    time.sleep(1)
    height=0
    while True:
        script = 'document.documentElement.scrollHeight'
        window.execute_script(f"window.scrollTo(0, {script});")
        time.sleep(5)
        action = window.execute_script(f"return {script}")
        if(height==action): break
        height=action
        continue
    iteration = []
    for element in window.find_elements('id', "video-title"):
        content = element.get_attribute('href')
        if(content==None): continue
        head = 'https://www.youtube.com/watch?v='
        body = content.split('?v=')[-1].split('&')[0]
        item = f'{head}{body}'
        iteration += [item]
        continue
    window.close()
    link = iteration    
    return(link)

def saveVideo(link, folder):
    os.makedirs(folder, exist_ok=True)
    name = link.split('?')[-1].split('=')[-1].split("&")[0]
    path = os.path.join(folder, name, 'video.mp4')
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

class Cloud:

    def __init__(self, channel, core):
        self.channel = channel
        self.core = core
        return

    def makeLink(self):
        link = getLink(self.channel, view=True)
        self.link = link
        return
    
    def saveLink(self):
        # tag = self.channel.split('=')[-1].split('&')[0]
        path = os.path.join(os.path.curdir, self.channel, 'link.txt')
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(f"{path}", 'w') as cache:
            for item in self.link: cache.write(f"{item}\n")
            pass
        print(f'Save link to [{path}].')
        return
    
    def saveVideo(self):
        folder = os.path.join(os.path.curdir, self.channel)
        pool = multiprocessing.Pool(self.core)
        tunnel = functools.partial(saveVideo, folder=folder)
        _ = pool.map(tunnel, self.link)
        pool.close()
        print(f'Save video to [{folder}].')
        return

    pass

if(__name__=='__main__'):
    definition = argparse.ArgumentParser()
    definition.add_argument(
        "--channel", 
        default="PLiY6wtxjK6QNoT1y7JFt_PEBNCrFI_Vux", 
        type=str
    )
    definition.add_argument("--core", default=8, type=int)
    argument = definition.parse_args()
    cloud = Cloud(argument.channel, argument.core)
    cloud.makeLink()
    cloud.saveLink()
    cloud.saveVideo()
    pass
