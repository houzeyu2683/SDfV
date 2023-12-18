# import glob
# import os
# import moviepy.editor

# folder = '主播焦點新聞/0001-0600/'
# iteration = glob.glob(f'{folder}/*/negative/*.mp4')
# for item in iteration:
#     # item = iteration[0]
#     print(item)
#     video = moviepy.editor.VideoFileClip(item)
#     video.write_videofile(
#         item, 
#         codec="libx264", 
#         logger=None, 
#         temp_audiofile=item.replace('.mp4', '.wav'),
#         fps=25    
#     )
#     continue

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--list", nargs="+", default=[0.1, 0.9], type=float)

value = parser.parse_args()
print(value.list)