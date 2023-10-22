import core

if(__name__=='__main__'):
    definition = core.argparse.ArgumentParser()
    definition.add_argument("--channel", default='youtube')
    definition.add_argument("--link")
    definition.add_argument("--folder")
    argument = definition.parse_args()
    channel = argument.channel #'youtube'
    link = argument.link #'https://www.youtube.com/playlist?list=PLbyorRThEk_J4xy8T95K_dtbJBtn0aG_8'
    folder = argument.folder #'./【年代新聞】2023年01-03月/'
    reptile = core.Reptile(channel=channel, folder=folder)
    inventory = reptile.getInventory(link=link)
    thread = 8
    pipe = core.Pipe(
        inventory=inventory, 
        channel=channel, 
        folder=folder
    )
    pipe.makeVideo(thread=thread)
    pass