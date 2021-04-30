import shutil
import os
from subprocess import check_call
import sys
from datetime import date, datetime
from yolo_check import clone_yolo
from convert_images import convert


# Clone Repository if yolov5 not already in the root folder
clone_yolo()

date = str(date.today())
time = datetime.now().strftime("%H_%M")

SOURCE = 'C:/Users/raeky/Documents/python_work/group_project_clearbot/test/SOURCE'
WEIGHTS = 'C:/Users/raeky/Documents/python_work/group_project_clearbot/prediction_pipeline/best.pt'
PROJECT = 'C:/Users/raeky/Documents/python_work/group_project_clearbot/test/' + date + '/'
NAME = 'predictions_' + time

try:
    os.mkdir(PROJECT)
except:
    pass

# Copy source images into date folder
if 'images' not in os.listdir(PROJECT):
    print('Copying images...\n')
    shutil.copytree(SOURCE, PROJECT + 'images')
    copied_source = PROJECT + 'images/'
    convert(copied_source, date)
else:
    if os.path.exists(PROJECT + 'images'):
        shutil.rmtree(PROJECT + 'images')
    shutil.copytree(SOURCE, PROJECT + 'images')
    copied_source = PROJECT + 'images/'
    convert(copied_source, date)
#     copied_source = PROJECT + 'images/'

source_count = len(os.listdir(SOURCE))
print(f'Source location is: {SOURCE}')
print(f'{source_count} images found in source folder.\n')

"""PREDICT"""
os.chdir('yolov5')
os.system(f'python detect.py --source {copied_source} --weights {WEIGHTS} --project {PROJECT} --name {NAME} --save-txt')

os.chdir(PROJECT + NAME)

# Copy bounded predictions to 'BOUNDED_IMAGES'
os.mkdir('bounded_images')
for file in os.listdir():
    if file[-4:] == '.jpg':
        shutil.move(file, 'bounded_images')


"""TKINTER"""



# # Install packages
# def install(package):
#     check_call([sys.executable, "-m", "pip", "install", package])

# # install('pygithub')



# # Model
# model = torch.hub.load('ultralytics/yolov5', 'custom', path_or_model='apr28pm50.pt')
# #model.load_state_dict(torch.load('apr28pm50.pt')['model'].state_dict())

# #model.classes = ['bottle', 'can', 'cup', 'box drink', 'face mask', 'plastic bag']

# import detect



# # Image
# img = 'C:/Users/raeky/Documents/python_work/group_project_clearbot/labelled_data/images/styro_62.jpg'


# detect.detect(img)

# img = Image.open(img)
# #print(img.size)
# #img.show()

# # Inference
# results = model(img)
# results.print()
#results.show()  # or .show(), .save()