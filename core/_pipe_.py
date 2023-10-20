import yt_dlp
import multiprocessing
import functools

def makeVideo(link, channel, folder):
    if(channel=='youtube'):
        identity = link.split('?')[-1].split('=')[-1].split("&")[0]
        option = {
            'quiet': True,
            'verbose': False,
            'progress': False,
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=mp4]/mp4',
            "outtmpl": f'{folder}/{identity}/video.mp4'
        }
        process = yt_dlp.YoutubeDL(option)
        _ = process.download(link)
        pass
    process.close()
    return

class Pipe:

    def __init__(self, link, channel):
        self.link = link
        self.channel = channel
        return

    def makeVideo(self, folder, thread=1):
        if(self.channel=='youtube'):
            process = multiprocessing.Pool(processes=thread)
            function = functools.partial(
                makeVideo, 
                channel=self.channel, 
                folder=folder
            )
            _ = process.map(function, self.link)
            pass
        process.close()
        return

    pass

