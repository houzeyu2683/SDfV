import core

link = 'https://www.youtube.com/playlist?list=PLSAUJHk8Limn1LuB8cgdPopFDG36px-Gg'

channel = 'youtube'
folder = './cache/'
route = 'https://www.youtube.com/watch?v='

reptile = core.Reptile(channel=channel, folder=folder)
inventory = reptile.getInventory(link=link)
print(f'Get {len(inventory)} inventory.')

link = [f'{route}{i}' for i in inventory[:16]]
thread = 4
pipe = core.Pipe(link=link, channel=channel)
pipe.makeVideo(folder=folder, thread=thread)

