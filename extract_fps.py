import cv2
import simplejson as json
import os
from pathlib import Path

def extract_fps_from_video(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    x = round(fps, ndigits=2)
    y = {"fps": x}
    print (y)
    return y

for root, dirs, files in os.walk("/home/user3/omer/repos/OmerAuto/videos/"):
    for dirname in dirs:
        z = extract_fps_from_video("/home/user3/omer/repos/OmerAuto/videos/"+dirname+"/video.mp4")
        with open("/home/user3/omer/repos/OmerAuto/videos/"+dirname+"/fps.json", 'w') as f:
            json.dump(z, f)
