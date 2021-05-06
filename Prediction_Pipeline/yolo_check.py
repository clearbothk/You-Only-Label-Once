import os
from subprocess import Popen, PIPE, STDOUT

def clone_yolo(YOLO):

    if YOLO[-6:] == 'yolov5':
        print('YOLOv5 folder found!\n')
    #if 'yolov5' not in os.listdir(YOLO):
    else:
        os.chdir(YOLO)
        print('YOLOv5 not found. Installing...\n')
        os.system("git clone https://github.com/ultralytics/yolov5")
        # url = "https://github.com/ultralytics/yolov5"  # Target clone repo address
        # proc = Popen(
        #     ["git", "clone", "--progress", url],
        #     stdout=PIPE, stderr=STDOUT, shell=True, text=True
        # )
        # for line in proc.stdout:
        #     if line:
        #         print(line.strip())  # Now you get all terminal clone output text
    # else:
    #     print('YOLOv5 folder found!\n')
        YOLO = os.getcwd() + '/yolov5'
    return YOLO