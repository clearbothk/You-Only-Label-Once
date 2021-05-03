from PIL import Image 

def crop_images(files, path, class_dict):

    for file in files:
        counter = 1
        label_path = path + '/labels/' + file + '.txt'
        im = Image.open(path + '/images/' + file + '.jpg')
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