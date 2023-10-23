import core

folder = './【主播焦點新聞】東森新聞/'
head = 0.01
tail = 0.8

detection = core.Detection(folder=folder, head=head, tail=tail)
detection.makeFragment(thread=4)
