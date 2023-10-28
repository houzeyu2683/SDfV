import threading
import time

def job(num, length=None):
    for n in num:
        print(f"Thread: {n}/{length}")
        time.sleep(1)
        continue
    # time.sleep(1)
    return

# threads = []
l1 = [i for i in range(100)]
l2 = [5,4,3,2,1]

j1 = threading.Thread(target = job, args = [l1])
j2 = threading.Thread(target = job, args = (l2, len(l2)))
j1.start()
j2.start()

j1.join()
j2.join()
# for i in range(5):
#   threads.append(threading.Thread(target = job, args = (i,)))
#   threads[i].start()

# # 主執行緒繼續執行自己的工作
# # ...

# # 等待所有子執行緒結束
# for i in range(5):
#   threads[i].join()

print("Done.")


# import os
# import moviepy.editor
# import time
# import PIL.Image
# import math 
# import multiprocessing
# import functools
# import numpy
# import tqdm
# import face_recognition
# import pathlib
# import glob

# class Recognition:

#     def __init__(self, image):
#         self.image = image
#         return
    
#     def makePrediction(self):
#         prediction = face_recognition.face_locations(self.image)
#         self.prediction = prediction

#     def getStatus(self):
#         length = len(self.prediction)
#         status = False if(length!=1) else True
#         return(status)
    
#     def getBox(self):
#         length = len(self.prediction)
#         box = None
#         if(length==1):
#             item = self.prediction[0]
#             top, right, bottom, left = item
#             box = left, top, right, bottom
#             pass
#         return(box)

#     def getCenter(self):
#         box = self.getBox()
#         center = [(box[0]+box[2])/2, (box[1]+box[3])/2]
#         return(center)

#     pass

# folder = "/home/houzeyu2683/Downloads/2/done/*/*.mp4"
# loop = glob.glob(folder)

# def checkVideo(path):
#     video = moviepy.editor.VideoFileClip(path)
#     for number, image in enumerate(video.iter_frames()):
#         recognition = Recognition(image=image)
#         recognition.makePrediction()
#         status = recognition.getStatus()
#         if(not status): 
#             print(status)
#             print(path)
#             print(number)
#             os.remove(path)
#             break
#         continue    
#     return

# pool = multiprocessing.Pool(4)
# pool.map(checkVideo, loop)


# # path = "/home/houzeyu2683/Downloads/2/00__done/7cz1jK4gSC4/320.mp4"
# # # 