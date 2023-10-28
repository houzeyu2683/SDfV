import core

if(__name__=='__main__'):
    definition = core.argparse.ArgumentParser()
    definition.add_argument("--channel", default='youtube')
    definition.add_argument("--link", default='https://www.youtube.com/playlist?list=PLbyorRThEk_J4xy8T95K_dtbJBtn0aG_8')
    definition.add_argument("--folder", default='./【年代新聞】2023年01-03月/')
    definition.add_argument("--thread", default=4)
    argument = definition.parse_args()
    channel = argument.channel
    link = argument.link
    folder = argument.folder
    reptile = core.Reptile(channel=channel, folder=folder)
    inventory = reptile.getInventory(link=link)
    pipe = core.Pipe(
        channel=channel, 
        folder=folder,
        inventory=inventory
    )
    thread = argument.thread
    pipe.makeVideo(thread=thread)
    pass