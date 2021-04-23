from tqdm import tqdm
import os
from PIL import Image

print("----------")
print("Converting all images to JPG format for processing")
print("----------")

raw_data = './raw_data/'
for pic in tqdm(os.listdir(raw_data)):
    if ('.txt' not in pic):
        name = pic.split('.')        
        im = Image.open(raw_data + pic)
        im = im.convert('RGB')
        im.save('./unlabeled_images/' + name[0] + '.jpg')