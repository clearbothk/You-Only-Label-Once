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
from relabel_correct_check_2 import correct_check
from crop_images import crop_images
from relabel_filter_app import filter_app
from relabel_read_stats import read_stats
from step5_combine_stats import combine_stats

# Variables -~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~

original_path = os.getcwd()
date = str(date.today())
time = datetime.now().strftime("%H_%M")

# Functions -~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~

def step1():
    global ic_images, ic_labels, c_relabel, ic_path
    # from load_source import load
    # global SOURCE, PROJECT, YOLO, NAME
    # SOURCE, PROJECT, YOLO = load(main)
    # print(SOURCE, PROJECT, YOLO)
    ic_path = filedialog.askdirectory()
    print(ic_path)
    ic_images = f'{ic_path}/images'
    ic_labels = f'{ic_path}/labels'

    os.chdir(ic_path)
    os.chdir('..')
    c_relabel = os.getcwd()
    os.makedirs("./relabel_Correct/",exist_ok=True)
    os.makedirs("./relabel_Correct/images",exist_ok=True)
    os.makedirs("./relabel_Correct/labels",exist_ok=True)
    os.makedirs("./relabel_Incorrect/",exist_ok=True)
    os.makedirs("./relabel_Incorrect/images",exist_ok=True)
    os.makedirs("./relabel_Incorrect/labels",exist_ok=True)
    os.makedirs("./relabel_Remove/",exist_ok=True)
    os.makedirs("./relabel_Remove/images",exist_ok=True)
    os.makedirs("./relabel_Remove/labels",exist_ok=True)
    # disable and set button text to 'Done' to indicate loading files and prediction has been completed
    # func1_text.set('Done')
    # func1_btn['state'] = 'disable'

def step2():
    """TKINTER"""
    correct_check(ic_images, ic_labels, main)

    """CROP IMAGES"""
    with open(original_path + '/item_classes.json') as f:
        item_class_dict = json.load(f)

    labels_path = glob.glob(ic_path + '/labels/*.txt')
    image_path = glob.glob(ic_path + '/images/*.jpg')
    #files = [i.split('/')[-1][:-4] for i in labels_path]
    files = [i[-25:-4] for i in labels_path]

    for cat in item_class_dict.values():
        os.makedirs(f'{c_relabel}/relabel_Correct/cropped/{cat}', exist_ok=True)

    crop_images(files, f'{c_relabel}/relabel_Correct', item_class_dict)

    # Should have a close button or have copy files automatically close window

def step3():
    path = f'{c_relabel}/relabel_Correct/cropped'
    filter_app(path, main)

def step4():
    path = f'{c_relabel}'
    os.chdir(path)
    read_stats(date,time)

def step5():
    print(os.getcwd())
    combine_stats(date)


# GUI application starts here -~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~

main = tk.Tk()
print('here 2')
main.geometry('700x800')
main.title('Relabel GUI')

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

intro = tk.Label(main, text='ClearBot Auto ReLabeling Program', font=('Calibri', 25))
intro.grid(column=0, columnspan=2, row=0)

func1_title = tk.Label(main, 
                        text='''Step 1. 
Select Input Relabeled Images Directory''', 
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
func4_btn = tk.Button(main, textvariable=func4_text, command=step4, height=4, width=30, borderwidth=5)
func4_text.set('Step 4')
func4_btn.grid(column=1, row=4)

func5_text = tk.StringVar()
func5_btn = tk.Button(main, textvariable=func5_text, command=step5, height=4, width=30, borderwidth=5)
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
