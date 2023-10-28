import core

if(__name__=='__main__'):
    definition = core.argparse.ArgumentParser()
    definition.add_argument("--folder", default='./video/')
    definition.add_argument("--head", default=0.01)
    definition.add_argument("--tail", default=0.9)
    definition.add_argument("--thread", default=4)
    argument = definition.parse_args()
    detection = core.Detection(
        folder=argument.folder, 
        head=argument.head, 
        tail=argument.tail
    )
    detection.makeFragment(thread=argument.thread)
    pass
