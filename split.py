import core

folder = './cache/'
detection = core.Detection(folder=folder)
detection.makeFragment(thread=4)