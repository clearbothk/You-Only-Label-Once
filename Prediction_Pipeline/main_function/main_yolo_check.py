import os

def clone_yolo(YOLO):
    if YOLO[-6:] == 'yolov5':
        print('YOLOv5 folder found!\n')
    else:
        os.chdir(YOLO)
        if 'yolov5' in os.listdir():
            print('YOLOv5 folder found!\n')
        else:
            print('YOLOv5 not found. Installing...\n')
            os.system("git clone https://github.com/ultralytics/yolov5")
        YOLO = os.getcwd() + '/yolov5'
    return YOLO