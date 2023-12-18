import argparse
import os
import moviepy.editor
import PIL.Image
import glob
import tqdm
import retinaface.RetinaFace
import pandas
import multiprocessing
import shutil
import hashlib
import numpy

video = moviepy.editor.VideoFileClip('YKcl07D6k4M_276.mp4')
video = video.set_fps(25)
clip = video.subclip(0, 0+1)
clip.duration
for index, _ in enumerate(clip.iter_frames()):
    print(index)
    continue