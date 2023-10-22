import core

folder = './【年代新聞】2023年01-03月/'
head = 0.01
tail = 0.8

detection = core.Detection(folder=folder, head=head, tail=tail)
detection.makeFragment(thread=1)
