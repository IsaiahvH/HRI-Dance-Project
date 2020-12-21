import time
import numpy as np
import pygame as pyg
import cv2
from pygame import movie

pose_names = ["air guitar", "clap your hands", "raise the roof", "hands on hips", "do the disco"]
pose_name_exception = ["give a box"]
videos = {}
# from: https://www.codegrepper.com/code-examples/python/python+split+video+into+frames
for pose_name in pose_names:
    full_video = f"C:/Users/lizzy/PycharmProjects/HRI-Dance-Project/Experiment/__pool__/poses/{pose_name}.mp4"
    vidcap = cv2.VideoCapture(full_video)
    success, image = vidcap.read()
    count = 0
    while success:
        current_frame = cv2.imwrite(f"C:/Users/lizzy/PycharmProjects/HRI-Dance-Project/Experiment/__pool__/poses/{pose_name}_frame%d.png" % count, image)
        print(pose_name)
        success, image = vidcap.read()
        print("read new frame: ", success)
        count += 1
        videos[pose_name] = current_frame

for pose_name in pose_name_exception:
    full_video = f"C:/Users/lizzy/PycharmProjects/HRI-Dance-Project/Experiment/__pool__/poses/{pose_name}.gif"
    vidcap = cv2.VideoCapture(full_video)
    success, image = vidcap.read()
    count = 0
    while success:
        current_frame = cv2.imwrite(f"C:/Users/lizzy/PycharmProjects/HRI-Dance-Project/Experiment/__pool__/poses/{pose_name}_frame%d.png" % count, image)
        print(pose_name)
        success, image = vidcap.read()
        print("read new frame: ", success)
        count += 1
        videos[pose_name] = current_frame



