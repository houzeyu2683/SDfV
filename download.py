import core

channel = 'youtube'
link = 'https://www.youtube.com/playlist?list=PLbyorRThEk_J4xy8T95K_dtbJBtn0aG_8'
folder = './【年代新聞】2023年01-03月/'

reptile = core.Reptile(channel=channel, folder=folder)
inventory = reptile.getInventory(link=link)

thread = 8
pipe = core.Pipe(
    inventory=inventory, 
    channel=channel, 
    folder=folder
)
pipe.makeVideo(thread=thread)

