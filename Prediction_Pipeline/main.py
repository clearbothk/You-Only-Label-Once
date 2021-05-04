import shutil
import os
import glob
import json
from PIL import Image
from datetime import date, datetime
from yolo_check import clone_yolo
from convert_images import convert, rename
from load_source import load_folder
from crop_images import crop_images
import subprocess

# Clone Repository if yolov5 not already in the root folder
"""CHECK YOLO"""
clone_yolo()

original_path = os.getcwd()
date = str(date.today())
time = datetime.now().strftime("%H_%M")

SOURCE = load_folder('Load Data Source')
WEIGHTS = original_path + '/best.pt'
PROJECT = load_folder('Load Project Folder')

while SOURCE == PROJECT:
    print('Source folder cannot be the same as destination folder!')
    PROJECT = load_folder('Load Project Folder')
 
PROJECT = PROJECT + '/' + date + '/'
NAME = 'predictions_' + time

try:
    os.mkdir(PROJECT)
except:
    pass

# Copy source images into date folder
if 'images' not in os.listdir(PROJECT):
    print('Copying images...\n')
else:
    if os.path.exists(PROJECT + 'images'):
        shutil.rmtree(PROJECT + 'images')
        shutil.rmtree(PROJECT + 'fullsize_images')

shutil.copytree(SOURCE, PROJECT + 'fullsize_images')
shutil.copytree(SOURCE, PROJECT + 'images')
copied_source = PROJECT + 'images/'
rename(PROJECT + 'fullsize_images/', date)
convert(copied_source, date)

source_count = len(os.listdir(SOURCE))
print(f'Source location is: {SOURCE}')
print(f'{source_count} images found in source folder.\n')

"""PREDICT"""
os.chdir('yolov5')
#os.system(f'python detect.py --source {copied_source} --weights {WEIGHTS} --project {PROJECT} --name {NAME} --save-txt --conf-thres 0.5')

subprocess = subprocess.Popen(f'python detect.py --source {copied_source} --weights {WEIGHTS} --project {PROJECT} --name {NAME} --save-txt --conf-thres 0.5', shell=True, stdout=subprocess.PIPE)
#subprocess_return = subprocess.stdout.read()
#print(subprocess_return)

while True:
  line = subprocess.stdout.readline()
  print(line.decode('utf-8').strip())
  if not line:
    break

os.chdir(PROJECT + NAME)

# Copy bounded predictions to 'BOUNDED_IMAGES'
try:
    os.mkdir('bounded_images')
except:
    pass
for file in os.listdir():
    if file[-4:] == '.jpg':
        shutil.move(file, 'bounded_images')

"""TKINTER"""
import correct_check

"""CROP IMAGES"""
with open(original_path + '/item_classes.json') as f:
    item_class_dict = json.load(f)

os.chdir('..')
os.chdir(os.getcwd() + '/' + NAME + '/Correct')
os.mkdir('cropped')

path = os.getcwd()

labels_path = glob.glob(path + '/labels/*.txt')
image_path = glob.glob(path + '/images/*.jpg')
#files = [i.split('/')[-1][:-4] for i in labels_path]
files = [i[-25:-4] for i in labels_path]

for cat in item_class_dict.values():
    os.mkdir('./cropped/' + cat)

crop_images(files, path, item_class_dict)

import filter_app


