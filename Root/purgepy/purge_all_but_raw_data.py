import os, glob
 
dir = '../unlabeled_images/'
filelist = glob.glob(os.path.join(dir, "*"))
for f in filelist:
    os.remove(f)

dir = '../labeled_images/labels'
filelist = glob.glob(os.path.join(dir, "*"))
for f in filelist:
    os.remove(f)

dir = '../labeled_images/images'
filelist = glob.glob(os.path.join(dir, "*"))
for f in filelist:
    os.remove(f)

dir = '../yolo_training_data/test/images'
filelist = glob.glob(os.path.join(dir, "*"))
for f in filelist:
    os.remove(f)

dir = '../yolo_training_data/test/labels'
filelist = glob.glob(os.path.join(dir, "*"))
for f in filelist:
    os.remove(f)

dir = '../yolo_training_data/train/images'
filelist = glob.glob(os.path.join(dir, "*"))
for f in filelist:
    os.remove(f)

dir = '../yolo_training_data/train/labels'
filelist = glob.glob(os.path.join(dir, "*"))
for f in filelist:
    os.remove(f)

dir = '../yolo_training_data/val/images'
filelist = glob.glob(os.path.join(dir, "*"))
for f in filelist:
    os.remove(f)

dir = '../yolo_training_data/val/labels'
filelist = glob.glob(os.path.join(dir, "*"))
for f in filelist:
    os.remove(f)