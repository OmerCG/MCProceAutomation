import cv2
import os
from pathlib import Path
Path.ls=lambda self : list(self.iterdir())
import subprocess
def extract_audio_from_video(video_file_in,audio_file_out=None , audio_type=None):
    video_file_in  = Path(video_file_in)
    if audio_file_out is None:
        if audio_type is None:
            audio_type = '.aac'
        audio_file_out =  video_file_in.with_suffix(audio_type)
    #'ffmpeg -i video.mp4 -map 0:0 -vn -acodec copy vidoe.aac'
    if audio_file_out.is_file():
        os.remove(str(audio_file_out))
    cmd = f'ffmpeg -i {str(video_file_in)} -map 0:0 -vn -acodec copy {audio_file_out}'
    s = subprocess.getstatusoutput(cmd)
    return audio_file_out , s

extract_audio_from_video('/home/user3/omer/repos/OmerAuto/20210120143522/video.mp4')

import os

for root, dirs, files in os.walk("/home/user3/omer/repos/OmerAuto/"):
    for dirname in dirs:
        extract_audio_from_video('/home/user3/omer/repos/OmerAuto/dirname/video.mp4')