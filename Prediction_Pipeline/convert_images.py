from tqdm import tqdm
import os
from PIL import Image, ImageOps


def convert(source, date):
    print("----------")
    print("Converting all images to JPG format for processing")
    print("----------")

    counter = 1

    for pic in tqdm(os.listdir(source)):
           
        im = Image.open(source + pic)
        im.thumbnail(size=(640, 640))
        im = ImageOps.exif_transpose(im)
        im = im.convert('RGB')
        im.save(f"{source}/{date}_image_{counter:04}.jpg")
        os.remove(source + pic)
        counter += 1