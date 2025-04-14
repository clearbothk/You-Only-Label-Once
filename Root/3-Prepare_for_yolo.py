import splitfolders
import os, glob
import time
import win32api



input_folder = './labeled_images'
output_folder = './yolo_training_data'


splitfolders.ratio(input_folder, output_folder, seed=42, ratio=(.7, .2, .1), group_prefix=None)



test_images = './yolo_training_data/test/images/'
test_images = len(glob.glob(os.path.join(test_images, "*")))


test_labels = './yolo_training_data/test/labels/'
test_labels = len(glob.glob(os.path.join(test_labels, "*")))


train_images = './yolo_training_data/train/images/'
train_images = len(glob.glob(os.path.join(train_images, "*")))


train_labels = './yolo_training_data/train/labels/'
train_labels = len(glob.glob(os.path.join(train_labels, "*")))


val_images = './yolo_training_data/val/images/'
val_images = len(glob.glob(os.path.join(val_images, "*")))


val_labels = './yolo_training_data/val/labels/'
val_labels = len(glob.glob(os.path.join(val_labels, "*")))

print("")

print(f"Test Images: {test_images}")
print(f"Test Labels: {test_labels}")

print(f"Train Images: {train_images}")
print(f"Train Labels: {train_labels}")

print(f"Val Images: {val_images}")
print(f"Val Labels: {val_labels}")

print("")
print(f"Total Images for Yolo Model: {test_images + train_images + val_images}")
print("")

test_if = [test_images != test_labels, train_images != train_labels, val_images != val_labels]

if any(test_if):
    print("Image and Label Counts DO NOT MATCH!")
    win32api.MessageBox(0, 'Image and Label Counts DO NOT MATCH!', 'ERROR')
else:
    print("Image and Label Counts Match")

time.sleep(5)