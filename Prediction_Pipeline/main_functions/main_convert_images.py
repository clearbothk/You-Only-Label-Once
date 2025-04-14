from tqdm import tqdm
import os
from PIL import Image, ImageOps


def convert(source, date):
    """Converts all input images to a max size of 640x640 pixels and copies into a
    folder called 'images'.

    Args:
        source (str): Source of the images
        date (str): Destination folder
    """
    print("----------")
    print("Converting all images to JPG format for processing")
    print("----------")

    counter = 1

    for pic in tqdm(os.listdir(source)):
        try:   
            im = Image.open(source + pic)
            im.thumbnail(size=(640, 640))
            im = ImageOps.exif_transpose(im)
            im = im.convert('RGB')
            im.save(f"{source}/{date}_image_{counter:04}.jpg")
            os.remove(source + pic)
            counter += 1
        except:
            pass

def rename(source, date):
    """Renames all input images and copies into a folder called 'fullsize_images'.

    Args:
        source ([str]): Source of the images
        date ([str]): Destination folder
    """
    print("----------")
    print("Renaming all source images for processing")
    print("----------")

    counter = 1

    for pic in tqdm(os.listdir(source)):
        try:  
            im = Image.open(source + pic)
            im = ImageOps.exif_transpose(im)
            im = im.convert('RGB')
            im.save(f"{source}/{date}_image_{counter:04}.jpg")
            os.remove(source + pic)
            counter += 1
        except:
            pass