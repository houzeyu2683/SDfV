import retinaface
import moviepy.editor

path = './6MEdVRAxCBI_156.mp4'
clip = moviepy.editor.VideoFileClip(path)
clip = clip.subclip(0, 1)

for index, _ in enumerate(clip.iter_frames(fps=25)):
    print(index)
    continue
clip = clip.set_fps(24.99)



retinaface.RetinaFace.detect_faces("img1.jpg")





# def changeVideo(path, folder):
#     # path = './video/source/1/USa2tmgBq_I_420.mp4'
#     clip = moviepy.editor.VideoFileClip(path)
#     print(clip.fps)
#     clip = clip.set_fps(24.99)
#     os.makedirs(folder, exist_ok=True)
#     clip.write_videofile(
#         os.path.join(folder, os.path.basename(path)), 
#         codec="libx264", 
#         audio_codec="aac",
#         temp_audiofile='./cache.mp4',
#         logger = None
#     )
#     return

# for path in tqdm.tqdm(glob.glob('./source/6/*.mp4')):
#     folder = os.path.dirname(path).replace("source", "source-new")
#     changeVideo(path, folder)
#     continue
