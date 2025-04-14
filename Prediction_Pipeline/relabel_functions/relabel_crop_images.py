from PIL import Image 

def crop_images(files, path, class_dict):
    """Takes all filtered images from Step 1 that have been identified as correct in Step 2
    and crops them according to the bounding box in preparation for material detection in Step 3.

    Args:
        files (list): List of files correctly predicted in Step 1
        path (str): Current Directory
        class_dict (dict): Dictionary of item classes from item_classes.json
    """
    for file in files:
        counter = 1
        label_path = path + '/labels/' + file + '.txt'
        try:
            im = Image.open(path + '/images/' + file + '.jpg')
        except:
            im = Image.open(path + '\images\\' + file + '.jpg')
        im = im.convert('RGB')
        im_w, im_h = im.size

        myfile=open(label_path,'r')
        myfile = myfile.readlines()
        
        for i in myfile:
            temp = i.split()
            item_class, x_center, y_center, w, h = [float(j.strip('\n')) for j in temp]
            item_class = str(int(item_class))

            x_cen = im_w * x_center 
            y_cen = im_h * y_center

            half_x = w * im_w / 2
            half_y = h * im_h / 2

            top_l = (x_cen - half_x, y_cen - half_y)
            bot_r = (x_cen + half_x, y_cen + half_y)

            area = (top_l[0], top_l[1], bot_r[0], bot_r[1])

            temp_pic = im.crop(area)
        
            temp_pic.save(f'{path}/cropped/{class_dict[item_class]}/{file}_{counter:02}.jpg')            
            counter += 1