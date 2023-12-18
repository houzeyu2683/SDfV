import shutil
import yt_dlp
import multiprocessing
import functools
import os

def makeVideo(link, channel, folder):
    if(channel=='youtube'):
        os.makedirs(folder, exist_ok=True)
        identity = link.split('?')[-1].split('=')[-1].split("&")[0]
        target = f'{folder}/{identity}/video.mp4'
        finish = os.path.isfile(target)
        if(finish): return
        shutil.rmtree(os.path.dirname(target), ignore_errors=True)
        option = {
            'quiet': True,
            'verbose': False,
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=mp4]/mp4',
            "outtmpl": f'{target}'
        }
        process = yt_dlp.YoutubeDL(option)
        try:_ = process.download(link)
        except: shutil.rmtree(os.path.dirname(target), ignore_errors=True)
        process.close()
        pass
    return

class Pipe:

    def __init__(self, inventory, channel, folder):
        self.inventory = inventory
        self.channel = channel
        self.folder = folder
        return

    def getIteration(self):
        if(self.channel=='youtube'):
            route = 'https://www.youtube.com/watch?v='
            iteration = [f'{route}{i}' for i in self.inventory]
            pass
        return(iteration)
    
    def makeVideo(self, thread=1):
        iteration = self.getIteration()
        process = multiprocessing.Pool(processes=thread)
        function = functools.partial(
            makeVideo, 
            channel=self.channel, 
            folder=self.folder,

        )
        _ = process.map(function, iteration)
        process.close()
        return
    
    pass
