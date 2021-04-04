from pathlib import Path
import os
import pandas as pd


#copying existing folders into a new folder
def copy_folder_names(origin_path,destination_path):
    list_of_folders = os.listdir(origin_path)
    for folder in list_of_folders:
        os.mkdir(os.path.join(destination_path, str(folder)+"_side_view"))
    return

#creating folders by video name:
def create_folders(csv_path,destination_path):
    df = pd.read_csv(csv_path)
    for folder in df['name']:
        os.mkdir(os.path.join(destination_path, folder))
    return