import glob
from tqdm import tqdm
import shutil
from PIL import Image

txt_dir = glob.glob("./just_bottles/*.txt")
class_target = ["4"]


txt_with_class_target = []

for txt in tqdm(txt_dir):
    with open(txt, "r") as f:
        text = f.readlines()
    for i in range(len(text)):
        if text[i].split()[0] in class_target:
            txt_with_class_target.append(txt)
            break


list_of_images = []
for i in range(len(txt_with_class_target)):
    test_image = txt_with_class_target[i].split("\\")[1][:-4]
    list_of_images.append(test_image)


for filename in list_of_images:
    #Grab Bounding Boxes in Each Txt file
    bounding_boxes = []
    with open(f"./just_bottles/{filename}.txt") as f:
        text = [line.strip().split() for line in f.readlines()]
        for line in text:
            if line[0] == "4":
                convert_to_float = [float(i) for i in line]
                bounding_boxes.append(convert_to_float)

    img = Image.open(f"./just_bottles/{filename}.jpg")
    for i in bounding_boxes:
        _, x, y, w, h = i

        left = int((x - w / 2) * dw)
        right = int((x + w / 2) * dw)
        top = int((y - h / 2) * dh)
        bottom = int((y + h / 2) * dh)
        im_cropped = img.crop((left, top, right, bottom))
        im_cropped.save(f"./test_delete/{filename}.jpg")

