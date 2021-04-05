from pathlib import Path
import os
import zipfile
import cv2
import simplejson as json
Path.ls=lambda self : list(self.iterdir())
import subprocess
import boto3
import pandas as pd

#creating folders by video name:
def create_folders(csv_path,destination_path):
    df = pd.read_csv(csv_path)
    for folder in df['name']:
        os.mkdir(os.path.join(destination_path, folder))
    return

#downloading the video and unziping it to the relevant folder
def unzipping_video_to_folder(video_path,bucket_name):
    s3 = boto3.client('s3')
    s3.download_file(bucket_name, video_path,'/home/user3/omer/data/mc-preprocess-data_v0.1.2/Tal/files.zip')
    video_id = Path(video_path).parts[-2]
    rootdir = Path('/home/user3/omer/data/mc-preprocess-data_v0.1.2/Tal')
    video_dir = str([video for video in rootdir.ls() if video_id in str(video)][0])
    with zipfile.ZipFile("/home/user3/omer/data/mc-preprocess-data_v0.1.2/Tal/files.zip", 'r') as zip_ref:
        zip_ref.extractall(video_dir)
    os.remove("/home/user3/omer/data/mc-preprocess-data_v0.1.2/Tal/files.zip")
    return

#extracting FPS from the video and creating a json file specifies the value
def extract_fps_from_video(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    x = round(fps, ndigits=2)
    y = {"fps": x}
    print (y)
    return y

#extracting the audio from the video
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


#path to csv file which contains the information of the videos and the destination directory
csv_path = '/home/user3/omer/data/Documentation/files_zip/temporary.csv'
destination_path = '/home/user3/omer/data/mc-preprocess-data_v0.1.2/Tal'
create_folders(csv_path,destination_path)

#define the bucket name and let the process begin
bucket_name = 'cg-ios-prealpha'

for video in (pd.read_csv(csv_path)['path']):
    path_to_video = str(video)
    print(f'processing video {path_to_video}')
    unzipping_video_to_folder(path_to_video,bucket_name)
    video_id = Path(path_to_video).parts[-2]
    rootdir = Path('/home/user3/omer/data/mc-preprocess-data_v0.1.2/Tal')
    video_directory = str([video for video in rootdir.ls() if video_id in str(video)][0])
    z = extract_fps_from_video(video_directory + "/video.mp4")
    with open(video_directory + "/fps.json", 'w') as f:
        json.dump(z, f)
    extract_audio_from_video(video_directory+"/video.mp4")







