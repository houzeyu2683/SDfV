import shutil
import yt_dlp
import multiprocessing
import functools
import os
import shutil

def makeVideo(link, channel, folder):
    print(f'Make [{link}] video.')
    if(channel=='youtube'):
        identity = link.split('?')[-1].split('=')[-1].split("&")[0]
        here = os.path.isfile(f'{folder}/{identity}/video.mp4')
        if(here): return
        history = os.path.isdir(f'{folder}/{identity}/')
        if(history): shutil.rmtree(f'{folder}/{identity}/')
        option = {
            'quiet': True,
            'verbose': False,
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=mp4]/mp4',
            "outtmpl": f'{folder}/{identity}/video.mp4'
        }
        process = yt_dlp.YoutubeDL(option)
        try:_ = process.download(link)
        except: shutil.rmtree(f'{folder}/{identity}/')
        pass
    process.close()
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
        if(self.channel=='youtube'):
            iteration = self.getIteration()
            if(thread<=1):
                for _, item in enumerate(iteration, start=1):
                    makeVideo(
                        link=item, 
                        channel=self.channel, 
                        folder=self.folder
                    )
                    continue
                pass
            else:
                process = multiprocessing.Pool(processes=thread)
                function = functools.partial(
                    makeVideo, 
                    channel=self.channel, 
                    folder=self.folder
                )
                _ = process.map(function, iteration)
                process.close()
                pass
            pass
        return

    pass

