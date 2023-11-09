import core

if(__name__=='__main__'):
    definition = core.argparse.ArgumentParser()
    definition.add_argument("--folder", default='', type=str)
    definition.add_argument("--scope", default=[0.01, 0.9], type=list)
    # definition.add_argument("--tail", default=0.9, type=float)
    definition.add_argument("--thread", default=4, type=int)
    argument = definition.parse_args()
    #
    folder = argument.folder
    head = argument.head
    tail = argument.tail
    thread = argument.thread
    #
    detection = core.Detection(
        folder=folder,
        head=head, 
        tail=tail
    )
    detection.makeFragment(thread=thread)
    pass
