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

dir = '../yolo_training_data/'
filelist = glob.glob(os.path.join(dir, "*"))
for f in filelist:
    os.remove(f)
