from pathlib import Path
import os
import zipfile
import cv2
import simplejson as json
Path.ls=lambda self : list(self.iterdir())
import subprocess
import boto3

########################## functions ####################################
def unzipping_video_to_folder(video_path,bucket_name):
    s3 = boto3.client('s3')
    s3.download_file(bucket_name, video_path,'/home/user3/omer/data/mc-preprocess-data_v0.1.0/files.zip')
    video_id = Path(video_path).parts[-2]
    rootdir = Path('/home/user3/omer/data/mc-preprocess-data_v0.1.0')
    video_dir = str([video for video in rootdir.ls() if video_id in str(video)][0])
    with zipfile.ZipFile("/home/user3/omer/data/mc-preprocess-data_v0.1.0/files.zip", 'r') as zip_ref:
        zip_ref.extractall(video_dir)
    os.remove("/home/user3/omer/data/mc-preprocess-data_v0.1.0/files.zip")
    return

def extract_fps_from_video(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    x = round(fps, ndigits=2)
    y = {"fps": x}
    print (y)
    return y

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
##########################################################################

#which video
path_to_video = "iphone/data/preAlpha/5fda0f13b5ac120d0e555830/603b9d542386eb6fe2150e9e/Take_5/20210228154829/files.zip"
bucket_name = 'cg-ios-prealpha'
video_id = Path(path_to_video).parts[-2]
rootdir = Path('/home/user3/omer/data/mc-preprocess-data_v0.1.0')
video_directory = str([video for video in rootdir.ls() if video_id in str(video)][0])

print(video_directory)
##### Unziping the folder, creating new folder with video_id name
unzipping_video_to_folder(path_to_video,bucket_name)

##### extracting fps and creating json file
z = extract_fps_from_video(video_directory+"/video.mp4")
with open(video_directory+"/fps.json", 'w') as f:
    json.dump(z, f)

#####extracting audio from the video
extract_audio_from_video(video_directory+"/video.mp4")