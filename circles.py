import cv2
import numpy as np
import vicosis_utils as utils
import time

start = time.time()

# fixed parameters
height = 1500
resolution = 240
frames = 200

video_path = r"C:\Users\adrhd\Videos\Captures\blade_runner_2049.mp4"
out_path = r'C:\Users\adrhd\Documents\GitHub\vicosis'

source = cv2.VideoCapture(video_path)
image = utils.process_avg(source, frames, height, circle=True, end_credits=15000)

cv2.imwrite(f"circles_{frames}f_{resolution}p_{time.time()-start:.2f}s.png", image)
