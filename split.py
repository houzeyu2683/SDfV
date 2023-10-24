import core

folder = './chunk/3/'
head = 0.00
tail = 1

detection = core.Detection(folder=folder, head=head, tail=tail)
detection.makeFragment(thread=1)
