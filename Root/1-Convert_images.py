from tqdm import tqdm
import os
from PIL import Image, ImageOps

print("----------")
print("Converting all images to JPG format for processing")
print("----------")

raw_images = './raw_images/'
for pic in tqdm(os.listdir(raw_images)): 
    if ('.txt' not in pic):
        name = pic.split('.')
        im = Image.open(raw_images + pic)
        im = im.convert('RGB')
        im = ImageOps.exif_transpose(im)
        im.save('./unlabeled_images/' + name[0] + '.jpg')