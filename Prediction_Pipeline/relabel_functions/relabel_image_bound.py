def img_bound(path_image, path_label, filename):
    import cv2
    
    img = cv2.imread(f'{path_image}/{filename}.jpg')
    dh, dw, _ = img.shape

    try:
        fl = open(f'{path_label}/{filename}.txt', 'r')
        data = fl.readlines()
        fl.close()
    except FileNotFoundError:
        print(f'No object(s) in {filename}.jpg')
        return

    for dt in data:
        object_class, x, y, w, h = map(float, dt.split(' '))
        l = int((x - w / 2) * dw)
        r = int((x + w / 2) * dw)
        t = int((y - h / 2) * dh)
        b = int((y + h / 2) * dh)

        object_dict = {   
            "0": "bottle", 
            "1": "can", 
            "2": "cup", 
            "3": "box_drink", 
            "4": "face_mask", 
            "5": "plastic_bag"
        }

        color_dict = {
            '0' : (49,203,69),
            '1' : (94,61,238),
            '2' : (219,159,43),
            '3' : (244,73,87),
            '4' : (192,228,219),
            '5' : (193,252,77)
        }
        # Split string to float

        if l < 0:
            l = 0
        if r > dw - 1:
            r = dw - 1
        if t < 0:
            t = 0
        if b > dh - 1:
            b = dh - 1
        
        cv2.rectangle(img, (l, t), (r, b), color_dict[str(int(object_class))], 2)
        cv2.rectangle(img, (l, t), (r,t-20), color_dict[str(int(object_class))], -1)
        cv2.putText(img, object_dict[str(int(object_class))], (l+5, t-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
    
    return img