import core

if(__name__=='__main__'):
    definition = core.argparse.ArgumentParser()
    definition.add_argument("--folder", default='', type=str)
    definition.add_argument("--scope", default=[0.01, 0.9], nargs='+', type=float)
    definition.add_argument("--thread", default=4, type=int)
    argument = definition.parse_args()
    #
    folder = argument.folder
    scope = argument.scope

    thread = argument.thread
    #
    detection = core.Detection(
        folder=folder,
        scope=scope
    )
    detection.makeFragment(thread=thread)
    pass
