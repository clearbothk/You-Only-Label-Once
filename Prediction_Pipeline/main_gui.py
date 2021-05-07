from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image
import tkinter as tk
import os
import glob
from time import localtime, strftime
import json
import shutil
from datetime import date, datetime

# import over .py file to call the functions-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~

from yolo_check import clone_yolo
from convert_images import convert, rename
from correct_check_main_gui import correct_check
from crop_images import crop_images
from filter_app_main_gui import filter_app

# Variables -~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~

original_path = os.getcwd()
date = str(date.today())
time = datetime.now().strftime("%H_%M")
print('here 1')
# Functions -~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~


def step1():
    from load_source import load
    global SOURCE, PROJECT, YOLO, NAME
    SOURCE, PROJECT, YOLO = load(main)
    print(SOURCE, PROJECT, YOLO)

    """CHECK YOLO"""
    YOLO = clone_yolo(YOLO)
    WEIGHTS = original_path + '/best.pt'
    PROJECT = PROJECT + '/' + date + '/'
    NAME = 'predictions_' + time
    
    print('check yolo done')
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

    # Create a popup to tell user that Step 2 ready
    mini_close = tk.Toplevel()
    mini_close.geometry('150x100')
    

    step1_name = tk.StringVar()
    step1_name.set('Step 1 Complete!')
    s1 = tk.Label(master=mini_close,textvariable=step1_name, font=('Calibri', 15))
    s1.grid(column=0, row=0)

    step1_close = tk.StringVar()
    step1_btn = tk.Button(mini_close, textvariable=step1_close, command=mini_close.destroy, height=2, width=10)
    step1_close.set('Close Window')
    step1_btn.grid(column=0, row=1)

    mini_close.mainloop()


def step2():
    """TKINTER"""
    path = PROJECT + NAME
    correct_check(path, main)

    """CROP IMAGES"""
    with open(original_path + '/item_classes.json') as f:
        item_class_dict = json.load(f)

    os.chdir('..')
    os.chdir(os.getcwd() + '/' + NAME + '/Correct')
    os.mkdir('cropped')

    path = os.getcwd()

    labels_path = glob.glob(path + '/labels/*.txt')
    image_path = glob.glob(path + '/images/*.jpg')
    #files = [i.split('/')[-1][:-4] for i in labels_path]
    files = [i[-25:-4] for i in labels_path]

    for cat in item_class_dict.values():
        os.mkdir('./cropped/' + cat)

    crop_images(files, path, item_class_dict)

    # Should have a close button or have copy files automatically close window

def step3():
    path = PROJECT + NAME
    filter_app(path + '/Correct/cropped', main)

def step4():
    pass

# GUI application starts here -~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~

main = tk.Tk()
print('here 2')
main.geometry('700x800')
main.title('Main GUI')

ico = Image.open('clearbot.png')
photo = ImageTk.PhotoImage(ico)
main.wm_iconphoto(False, photo)


# KeyBinding Controls
# root.bind("<Key>", handle_keypress)
# root.bind("<Left>", left)
# root.bind('<Right>', right)
# root.bind('<Escape>', quitquit)
# root.bind('<BackSpace>', deldel)
# root.bind('<Shift-BackSpace>', deldelclean)
# root.bind('<Delete>', deldel)
# root.bind('<Shift-Delete>', deldelclean)
# root.bind('<Up>', up)
# root.bind('<Down>', down)

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
                        text='''Step 5.
''', 
                        justify='left',
                        anchor=W,
                        width=45,
                        height=6,
                        font=('Calibri', 12))
func5_title.grid(column=0, row=5)

# func6_title = tk.Label(root, text='None')
# func6_title.grid(column=0, row=6)

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
func4_btn = tk.Button(main, textvariable=func4_text, height=4, width=30, borderwidth=5)
func4_text.set('Step 4')
func4_btn.grid(column=1, row=4)

func5_text = tk.StringVar()
func5_btn = tk.Button(main, textvariable=func5_text, height=4, width=30, borderwidth=5)
func5_text.set('Step 5')
func5_btn.grid(column=1, row=5)

# func6_text = tk.StringVar()
# func6_btn = tk.Button(root, textvariable=func6_text, command=lambda:test('empty'))
# func6_text.set('func 6')
# func6_btn.grid(column=6, row=0)

# func7_text = tk.StringVar()
# func7_btn = tk.Button(root, textvariable=func7_text, command=lambda:test('empty'))
# func7_text.set('func 7')
# func7_btn.grid(column=6, row=1)

# func8_text = tk.StringVar()
# func8_btn = tk.Button(root, textvariable=func8_text, command=lambda:test('empty'))
# func8_text.set('func 8')
# func8_btn.grid(column=6, row=2)

# func9_text = tk.StringVar()
# func9_btn = tk.Button(root, textvariable=func9_text, command=lambda:test('empty'))
# func9_text.set('func 9')
# func9_btn.grid(column=6, row=3)

# func10_text = tk.StringVar()
# func10_btn = tk.Button(root, textvariable=func10_text, command=lambda:test('empty'))
# func10_text.set('func 10')
# func10_btn.grid(column=6, row=4)

# func11_text = tk.StringVar()
# func11_btn = tk.Button(root, textvariable=func11_text, command=lambda:test('empty'))
# func11_text.set('func 11')
# func11_btn.grid(column=6, row=5)

# finish
main.mainloop()
