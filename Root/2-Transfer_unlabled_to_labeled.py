import glob
import shutil
from tqdm import tqdm
import os


print("----------")
print("Transfering all unlabeled to labled")
print("----------")

#Sort Labeled Images from "unlabled_images" to "labeled_images"
labeled_txt = glob.glob("./unlabeled_images/*.txt")
file_names = []
for txt in tqdm(labeled_txt):
    file_name = txt.split("\\")[-1][:-4]
    file_names.append(file_name)

#move all images and text in file_names to /labeled_images/images AND /labeled_images/label
for file in tqdm(file_names):
    try:
        shutil.move("./unlabeled_images/"+file+".jpg", f"./labeled_images/images/{file}.jpg")
    except:
        pass
    try:
        shutil.move("./unlabeled_images/"+file+".txt", f"./labeled_images/labels/{file}.txt")
    except:
        pass