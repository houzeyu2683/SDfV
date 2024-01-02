import selenium.webdriver
import time
import os
import multiprocessing
import shutil
import yt_dlp
import functools
import argparse

def saveVideo(link, folder):
    os.makedirs(folder, exist_ok=True)
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

    def __init__(self, channel):
        self.channel = channel
        return

    def makeLink(self):
        option = selenium.webdriver.ChromeOptions()
        option.add_argument("--headless")
        web = selenium.webdriver.Chrome(options=option)
        web.get(self.channel)
        time.sleep(1)
        height=0
        while True:
            script = 'document.documentElement.scrollHeight'
            web.execute_script(f"window.scrollTo(0, {script});")
            time.sleep(0.5)
            action = web.execute_script(f"return {script}")
            if(height==action):break
            else: height=action
            continue
        iteration = []
        for element in web.find_elements('id', "video-title"):
            content = element.get_attribute('href')
            if(content==None): continue
            head = 'https://www.youtube.com/watch?v='
            body = content.split('?v=')[-1].split('&')[0]
            item = f'{head}{body}'
            iteration += [item]
            continue
        web.close()
        self.link = iteration
        return
    
    def saveLink(self):
        tag = self.channel.split('=')[-1].split('&')[0]
        path = os.path.join(os.path.curdir, tag, 'link.txt')
        os.makedirs(os.path.dirname(path), exist_ok=True)
        archive = open(f"{path}", 'w')
        for item in self.link: archive.write(f"{item}\n")
        archive.close()
        return
    
    def saveVideo(self, core):
        tag = self.channel.split('=')[-1].split('&')[0]
        folder = os.path.join(os.path.curdir, tag)
        pool = multiprocessing.Pool(core)
        function = functools.partial(saveVideo, folder=folder)
        _ = pool.map(function, self.link)
        pool.close()
        return

    pass

if(__name__=='__main__'):
    definition = argparse.ArgumentParser()
    definition.add_argument("--channel", default="", type=str)
    definition.add_argument("--core", default=4, type=int)
    argument = definition.parse_args()
    media = Media(channel=argument.channel)
    media.makeLink()
    media.saveLink()
    media.saveVideo(core=argument.core)
    pass
