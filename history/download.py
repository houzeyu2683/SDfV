import core

if(__name__=='__main__'):
    #
    definition = core.argparse.ArgumentParser()
    definition.add_argument("--channel", default='youtube', type=str)
    definition.add_argument("--link", default='', type=str)
    definition.add_argument("--folder", default='', type=str)
    definition.add_argument("--thread", default=4, type=int)
    argument = definition.parse_args()
    #
    channel = argument.channel
    link = argument.link
    folder = argument.folder
    thread = argument.thread
    #
    reptile = core.Reptile(channel=channel, folder=folder)
    inventory = reptile.getInventory(link=link)
    pipe = core.Pipe(
        channel=channel, 
        folder=folder,
        inventory=inventory
    )
    pipe.makeVideo(thread=thread)
    pass