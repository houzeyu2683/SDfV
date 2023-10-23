import core

channel = 'youtube'
link = 'https://www.youtube.com/playlist?list=PLbyorRThEk_LczvBPiBDNaejrjGQILDTO'
folder = './【年代新聞】2023年04-06月/'

reptile = core.Reptile(channel=channel, folder=folder)
inventory = reptile.getInventory(link=link)

thread = 8
pipe = core.Pipe(
    inventory=inventory, 
    channel=channel, 
    folder=folder
)
pipe.makeVideo(thread=thread)

