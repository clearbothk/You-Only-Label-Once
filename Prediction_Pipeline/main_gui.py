from tkinter import *
from PIL import ImageTk, Image
import tkinter as tk
import os
import glob
import json
import shutil
from datetime import date, datetime

# import over .py file to call the functions-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~

from main_function.main_yolo_check import clone_yolo
from main_function.main_convert_images import convert, rename
from main_function.main_crop_images import crop_images
from main_function.main_correct_check import correct_check
from main_function.main_filter_app import filter_app
from main_function.main_read_stats import read_stats
from main_function.main_combine_stats import combine_stats
from main_function.main_load_source import load

# Variables -~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~

original_path = os.getcwd()
date = str(date.today())
time = datetime.now().strftime("%H_%M")

# Functions -~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~


def step1():
    global SOURCE, PROJECT, YOLO, NAME
    SOURCE, PROJECT, YOLO = load(main)

    """CHECK YOLO"""
    YOLO = clone_yolo(YOLO)
    WEIGHTS = original_path + '/best.pt'
    PROJECT = PROJECT + '/' + date + '/'
    NAME = 'predictions_' + time
    
    try:
        os.mkdir(PROJECT)
    except:
        pass

    # Copy source images into date folder
    if 'images' and 'fullsize_images' not in os.listdir(PROJECT):
        print('Copying images...\n')
    else:
        if os.path.exists(PROJECT + 'images') or os.path.exists(PROJECT + 'fullsize_images'):
            try:
                shutil.rmtree(PROJECT + 'images')
                shutil.rmtree(PROJECT + 'fullsize_images')
            except FileNotFoundError:
                pass

    shutil.copytree(SOURCE, PROJECT + 'fullsize_images')
    shutil.copytree(SOURCE, PROJECT + 'images')
    copied_source = PROJECT + 'images/'
    rename(PROJECT + 'fullsize_images/', date)
    convert(copied_source, date)

    source_count = len(os.listdir(SOURCE))
    print(f'Source location is: {SOURCE}')
    print(f'{source_count} images found in source folder.\n')

    """PREDICT"""
    os.chdir(YOLO)
    os.system(f'python detect.py --source {copied_source} --weights {WEIGHTS} --project {PROJECT} --name {NAME} --save-txt --conf-thres 0.6 --line-thickness 1')

    os.chdir(PROJECT + NAME)
    
    # Copy bounded predictions to 'BOUNDED_IMAGES'
    try:
        os.mkdir('bounded_images')
    except:
        pass
    for file in os.listdir():
        if file[-4:] == '.jpg':
            shutil.move(file, 'bounded_images')

    # disable and set button text to 'Done' to indicate loading files and prediction has been completed
    func1_text.set('Done')
    func1_btn['state'] = 'disable'

def step2():
    """TKINTER"""
    correct_check(PROJECT, NAME, main)

    """CROP IMAGES"""
    with open(original_path + '/item_classes.json') as f:
        item_class_dict = json.load(f)

    os.chdir('..')
    os.chdir(os.getcwd() + '/' + NAME + '/Correct')
    os.mkdir('cropped')

    path = os.getcwd()

    labels_path = glob.glob(path + '/labels/*.txt')
    files = [i[-25:-4] for i in labels_path]

    for cat in item_class_dict.values():
        os.mkdir('./cropped/' + cat)

    crop_images(files, path, item_class_dict)

    # Should have a close button or have copy files automatically close window

def step3():
    filter_app(f'{PROJECT}{NAME}/Correct/cropped', main)

def step4():
    read_stats(PROJECT + NAME,date,time)

def step5():
    combine_stats(date)

# GUI application starts here -~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~

main = tk.Tk()
main.geometry('700x800')
main.title('Main GUI')

ico = Image.open('clearbot.png')
photo = ImageTk.PhotoImage(ico)
main.wm_iconphoto(False, photo)

# Setting Canvas
canvas_main = tk.Canvas(main, width=700, height=750)
canvas_main.grid(columnspan=2, rowspan=6)

# Instructions

intro = tk.Label(main, text='ClearBot Auto Labeling Program', font=('Calibri', 25))
intro.grid(column=0, columnspan=2, row=0)

func1_title = tk.Label(main, 
                        text='''Step 1. 
Select Input Directory (Source)
Select Output Directory (Destination)
Select YOLOv5 Installation Directory (YOLO)''', 
                        justify='left', 
                        anchor=W, 
                        width=45,
                        height=6,
                        font=('Calibri', 12))
func1_title.grid(column=0, row=1)

func2_title = tk.Label(main, 
                        text='''Step 2.
Filter Images by Correct and Incorrect
'Correct' image has all objects bounded correctly.
'Incorrect' image has poorly bounded or missed objects.
'Remove' image is for unwanted photos.
'Copy Files' when complete.''', 
                        justify='left', 
                        anchor=W, 
                        width=45,
                        height=6,
                        font=('Calibri', 12))
func2_title.grid(column=0, row=2)

func3_title = tk.Label(main, 
                        text='''Step 3.
Filter objects by material
Make sure to copy files for each category before 
moving to the next.
''', 
                        justify='left',
                        anchor=W,
                        width=45,
                        height=6,
                        font=('Calibri', 12))
func3_title.grid(column=0, row=3)

func4_title = tk.Label(main, 
                        text='''Step 4.
Display statistics for current batch of images''', 
                        justify='left',
                        anchor=W,
                        width=45,
                        height=6,
                        font=('Calibri', 12))
func4_title.grid(column=0, row=4)

func5_title = tk.Label(main, 
                        text=f'''Step 5.
Show {date} Stats
''', 
                        justify='left',
                        anchor=W,
                        width=45,
                        height=6,
                        font=('Calibri', 12))
func5_title.grid(column=0, row=5)

# Function buttons

func1_text = tk.StringVar()
func1_btn = tk.Button(main, textvariable=func1_text, command=step1, height=4, width=30, borderwidth=5)
func1_text.set('Step 1')
func1_btn.grid(column=1, row=1)

func2_text = tk.StringVar()
func2_btn = tk.Button(main, textvariable=func2_text, command=step2, height=4, width=30, borderwidth=5)
func2_text.set('Step 2')
func2_btn.grid(column=1, row=2)

func3_text = tk.StringVar()
func3_btn = tk.Button(main, textvariable=func3_text, command=step3, height=4, width=30, borderwidth=5)
func3_text.set('Step 3')
func3_btn.grid(column=1, row=3)

func4_text = tk.StringVar()
func4_btn = tk.Button(main, textvariable=func4_text, command=step4, height=4, width=30, borderwidth=5)
func4_text.set('Step 4')
func4_btn.grid(column=1, row=4)

func5_text = tk.StringVar()
func5_btn = tk.Button(main, textvariable=func5_text, command=step5, height=4, width=30, borderwidth=5)
func5_text.set('Step 5')
func5_btn.grid(column=1, row=5)

# finish
main.mainloop()
