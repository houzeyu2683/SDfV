import core

link = 'https://www.youtube.com/playlist?list=PLp7hnLHxd1KHrp5YZtbQXp2cRS3UGsnQS'

channel = 'youtube'
folder = './PLp7hnLHxd1KHrp5YZtbQXp2cRS3UGsnQS/'

reptile = core.Reptile(channel=channel, folder=folder)
inventory = reptile.getInventory(link=link)

thread = 8
pipe = core.Pipe(
    inventory=inventory, 
    channel=channel, 
    folder=folder
)
pipe.makeVideo(thread=thread)

