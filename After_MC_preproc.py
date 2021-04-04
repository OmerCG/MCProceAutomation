import os
import os.path
from os import path
import shutil
from pathlib import Path
import zipfile
import cv2
import simplejson as json
import subprocess
import boto3
import pandas as pd
Path.ls=lambda self : list(self.iterdir())

def unzipping_MC_to_folder(video_path,bucket_name):
    s3 = boto3.client('s3')
    s3.download_file(bucket_name, video_path, '/home/user3/omer/data/mc-preprocess-data_v0.1.2/Tal/motion_capture_preprocess.zip')
    video_id = Path(video_path).parts[-2]
    rootdir = Path('/home/user3/omer/data/mc-preprocess-data_v0.1.2/Tal')
    video_dir = str([video for video in rootdir.ls() if video_id in str(video)][0])
    with zipfile.ZipFile("/home/user3/omer/data/mc-preprocess-data_v0.1.2/Tal/motion_capture_preprocess.zip", 'r') as zip_ref:
        zip_ref.extractall("/home/user3/omer/data/mc-preprocess-data_v0.1.2/Tal")
    if path.isdir("/home/user3/omer/data/mc-preprocess-data_v0.1.2/Tal/motion_capture_preprocess_output/proc_res") == True:
        shutil.move("/home/user3/omer/data/mc-preprocess-data_v0.1.2/Tal/motion_capture_preprocess_output/proc_res",
                    video_dir)
        shutil.move("/home/user3/omer/data/mc-preprocess-data_v0.1.2/Tal/motion_capture_preprocess_output/frames",
                    video_dir)
    else:
        shutil.move("/home/user3/omer/data/mc-preprocess-data_v0.1.2/Tal/motion_capture_preprocess/motion_capture_preprocess_output/proc_res",
                    video_dir)
        shutil.move("/home/user3/omer/data/mc-preprocess-data_v0.1.2/Tal/motion_capture_preprocess/motion_capture_preprocess_output/frames",
                    video_dir)
    shutil.move(video_dir + "/fps.json", video_dir + "/proc_res")
    shutil.move(video_dir + "/video.aac", video_dir + "/proc_res")
    shutil.move(video_dir + "/video.mp4", video_dir + "/proc_res")
    if path.isfile(video_dir + "/version_0_1_0") == True:
        shutil.move(video_dir + "/version_0_1_0", video_dir + "/proc_res")
    if path.isfile(video_dir + "/Output.txt") == True:
        shutil.move(video_dir + "/Output.txt", video_dir + "/proc_res")
    os.remove("/home/user3/omer/data/mc-preprocess-data_v0.1.2/Tal/motion_capture_preprocess.zip")
    if path.isdir("/home/user3/omer/data/mc-preprocess-data_v0.1.2/Tal/motion_capture_preprocess_output") == True:
        os.rmdir("/home/user3/omer/data/mc-preprocess-data_v0.1.2/Tal/motion_capture_preprocess_output")
    if path.isdir("/home/user3/omer/data/mc-preprocess-data_v0.1.2/Tal/motion_capture_preprocess") == True:
        os.rmdir("/home/user3/omer/data/mc-preprocess-data_v0.1.2/Tal/motion_capture_preprocess")
    return

#####In order to run the videos one by one uncomment the following lines#####

# path_to_video = "iphone/data/preAlpha/5fda0f13b5ac120d0e555830/6062eac02386eb6fe2150fc5/Take_0/20210330120939/motion_capture_preprocess.zip"
# print(f'processing video {path_to_video}')
# video_bucket = 'cg-trueself-artifacts'
# unzipping_MC_to_folder(path_to_video,video_bucket)

#####In order to run all of the videos uncomment the following lines#####

csv_path = '/home/user3/omer/data/Documentation/mc_preprocess_zip/temporary_MC.csv'
video_bucket = 'cg-trueself-artifacts'
for video in (pd.read_csv(csv_path)['path']):
    path_to_video = str(video)
    print(f'processing video {path_to_video}')
    unzipping_MC_to_folder(path_to_video,video_bucket)