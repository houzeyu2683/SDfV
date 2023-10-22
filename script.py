# import yt_dlp
# import face_recognition
# import moviepy.editor
# import time
# import selenium
# import selenium.webdriver
# import chromedriver_autoinstaller
# import PIL.Image
# import tqdm
# #
# def getIndex(link):
#     _ = chromedriver_autoinstaller.install()
#     option = selenium.webdriver.ChromeOptions()
#     option.add_argument("--headless")
#     driver = selenium.webdriver.Chrome(options=option)
#     driver.get(link)
#     time.sleep(5)
#     #
#     height = driver.execute_script("return document.documentElement.scrollHeight")
#     while True:
#         script = f"window.scrollTo(0, document.documentElement.scrollHeight);"
#         driver.execute_script(script)
#         time.sleep(1)
#         update = driver.execute_script("return document.documentElement.scrollHeight")
#         if(height==update):break
#         else: height=update
#         continue
#     #
#     index = []
#     for item in driver.find_elements('id', "video-title"):
#         content = item.get_attribute('href')
#         if(content): index += [content.split('?v=')[-1]]
#         continue
#     return(index)

# def getDetection(image):
#     prediction = face_recognition.face_locations(image)
#     if(prediction==[] or len(prediction)>1):
#         box, status = None, False
#         pass
#     else:
#         box, status = prediction[0], True
#         top, right, bottom, left = box
#         box = left, top, right, bottom
#         pass
#     detection = box, status
#     return(detection)

# class Engine:
#     # index = "__rJ_BVZRSA"
#     # link = https://www.youtube.com/watch?v=JYqWZmAMuPM
#     def __init__(self, link='https://www.youtube.com/watch?v=JYqWZmAMuPM', folder='./cache'):
#         self.link = link
#         self.folder = folder
#         return

#     def downloadVideo(self):
#         index = self.link.split("?v=")[-1].split('&')[0]
#         option = {
#             'verbose': False,
#             'format': 'bestvideo[ext=mp4]+bestaudio[ext=mp4]/mp4',
#             "outtmpl": f'{self.folder}/{index}/video.mp4'
#         }
#         with yt_dlp.YoutubeDL(option) as process: process.download(self.link)
#         return
    
#     def extractVideo(self):
#         index = self.link.split("?v=")[-1].split('&')[0]
#         path = f'{self.folder}/{index}/video.mp4'
#         video = moviepy.editor.VideoFileClip(path)
#         width, height = video.size
#         length = int(video.duration)
#         for second in range(length):
#             if(second<(length*0.1) or second>(length*0.9)): continue
#             image = video.get_frame(second)
#             box, status = getDetection(image)
#             if(status): 
#                 image = video.get_frame(second+1)
#                 _, status = getDetection(image)
#                 pass
#             if(status): 
#                 lock = video.subclip(second, second+1)
#                 limit = max(box[2] - box[0], box[3] - box[1])
#                 area = (box[2] - box[0]) * (box[3] - box[1])
#                 if(area>96*96): 
#                     lock = lock.crop(
#                         x1=max(0, box[0]-limit),
#                         y1=max(0, box[1]-limit),
#                         x2=min(width, box[2]+limit),
#                         y2=min(height, box[3]+limit)
#                     )
#                     time.sleep(1)
#                     lock.write_videofile(f'{self.folder}/{index}/{second}.mp4', codec="libx264", logger=None)
#                     PIL.Image.fromarray(lock.get_frame(0)).save(f'{self.folder}/{index}/{second}.jpg')
#                     pass
#                 pass
#             number = second+1
#             print(f'{number}/{length}', end='\r')
#             continue
#         video.close()
#         return
    
#     pass
# link = "https://www.youtube.com/@chinatvnews/search?query=中視新聞全球報導"
# # link = "https://www.youtube.com/playlist?list=PLp7hnLHxd1KFmDKEV3AMpCrNW21Nz9AVT"
# index = getIndex(link)
# length = len(index)
# mark = [
#     "4OxUKzAPQA8", "5fN6KQDh6kA", '7QHccK753IU', '19iVXzaQiFc', "42jtSODIqGs",
#     'BxCUCsKhMHE', 'dnphcBG-q1M', 'Hb3ZaGBtv5U', 'ht1qlZQgDxA', "Ip-oCJREYow",
#     'IXe1OjmF65w', 'KN2Cfv_YeqM', 'MHli0ECwtyQ', 'O2X8yx4miCs', 'OUVNgQSNZko', 
#     'qjo7J2NS248', "qRzuP9hdoH0", "SoyyH4H86wQ",
#     "tdXnLwvm8J0", "TJooA_b52Nk", "TjpusbNxGvA", 'TnAQRlh7NIU', 'Wk45EB0OHC8', "x0-vACQ1HFw", 
#     "XSQn_l_tvqU",
#     "Y07SKPG8-t8"
# ]
# for n, i in enumerate(index, start=1):
#     print(f"{n}/{length}")
#     if(i in mark): continue
#     engine = Engine(link=f'https://www.youtube.com/watch?v={i}', folder='./cache/')
#     engine.downloadVideo()
#     engine.extractVideo()
#     continue
