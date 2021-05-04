from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image
import tkinter as tk
import os
import glob
from time import localtime, strftime
import json
import shutil

# Variables -~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~

# dict for materials lists for record and use when moving files
material_dict = {
    'Plastic' : [],
    'Metal' : [],
    'Styrofoam' : [],
    'Glass' : [],
    'Paper' : [],
    'Unknown' : []
}

object_material = {
    'Bottle' : ['Plastic', 'Glass'],
    'Can' : [],
    'Cup' : ['Styrofoam', 'Plastic', 'Paper'],
    'Box Drink' : [], 
    'Face Mask' : [], 
    'Plastic Bag' : []
}

list_dir = ['']

object_list = ['bottle', 'can', 'cup', 'box_drink', 'face_mask', 'plastic_bag', 'utensils']
object_class = '_______'

# Functions -~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~

# read folders from directory
def open_directory():
    global root_dir
    global list_dir
    global root_path
    global dir_dict
    global prediction_folder
    root_dir = filedialog.askdirectory(title='Please Select Cropped Objects Folder')
    os.chdir(root_dir)
    root_path = os.getcwd()
    os.chdir('..')
    os.chdir('..')
    prediction_folder = os.getcwd()
    list_dir = [i for i in os.listdir(root_dir) if i.lower() in object_list]
    dir_dict = {}

    # create dictionary for object directory paths
    for i in list_dir:
        dir_dict[i] = f'{root_path}/{i}'

    # Reset object_menu and delete all old options
    object_menu.set('')
    w['menu'].delete(0, 'end')

    # Insert list of new options (tk._setit hooks them up to var)
    for i in list_dir:
        w['menu'].add_command(label=i, command=tk._setit(object_menu, i, change_folder))
    
    object_menu.set(list_dir[0])
    open_file_multi(dir_dict[object_menu.get()])

def change_folder(event):
    global object_menu
    global list_dir
    open_file_multi(dir_dict[object_menu.get()])
    
# object_menu = StringVar()
# object_menu.set('empty') # default value
# w = OptionMenu(root, object_menu, *list_dir, command=test)
# w.grid(column=0,row=0)

def open_file_multi(dir_path):
    #using global to create a global variable
    global list_images
    global image_dict
    global folder_path
    global current_image
    global folder
    global object_class
    global material_dict

    # clicking button allows user to select specific directory
    folder = dir_path

    # create list of image filenames 
    list_images = sorted(os.listdir(folder)) 
    list_images = [i for i in list_images if '.jpg' in i] # names of images into a list
    os.chdir(folder)
    folder_path = os.getcwd()

    # display what object class the folder belongs to and to control whether materials can be selected
    for i in object_list:
        if i.lower() in folder_path.lower():
            object_class = i
            instructions['text'] = f'Please select the what material the {object_class} is made of'
            break
        else:
            object_class = 'Unknown Object'
            instructions['text'] = f'Please select the what material the {object_class} is made of'
    
    # image filename dictionary for counting reference
    image_dict = {}
    for i in range(len(list_images)):
        image_dict[i] = list_images[i]
    print(f'{len(list_images)} image(s) in this folder')

    material_dict = {
    'Plastic' : [],
    'Metal' : [],
    'Styrofoam' : [],
    'Glass' : [],
    'Paper' : [],
    'Unknown' : []
}
    # load material_dict if in folder (continue to work if work has already been done) else create material_dict.json 
    if f'{object_class}_material_dict.json' in os.listdir(folder):
        load_dict()
        print(f'material dictionary found, {object_class}_material_dict.json loaded')
    else:
        save_dict()
        print(f'material dictionary not found, {object_class}_material_dict.json created and saved')

    # load first image filename_text and fileclass_text
    current_image = 0
    load_image()
    save_dict()
    count_class()

def open_file():
    #using global to create a global variable
    global list_images
    global image_dict
    global folder_path
    global current_image
    global folder
    global object_class

    # clicking button allows user to select specific directory
    folder = filedialog.askdirectory()

    # create list of image filenames 
    list_images = sorted(os.listdir(folder)) 
    list_images = [i for i in list_images if '.jpg' in i] # names of images into a list
    os.chdir(folder)
    folder_path = os.getcwd()
    print(folder_path)

    # display what object class the folder belongs to and to control whether materials can be selected
    for i in object_list:
        if i.lower() in folder_path.lower():
            object_class = i
            instructions['text'] = f'Please select the what material the {object_class} is made of'
        else:
            object_class = 'Unknown Object'
            instructions['text'] = f'Please select the what material the {object_class} is made of'
    
    # image filename dictionary for counting reference
    image_dict = {}
    for i in range(len(list_images)):
        image_dict[i] = list_images[i]
    print(f'{len(list_images)} image(s) in this folder')

    # load material_dict if in folder (continue to work if work has already been done) else create material_dict.json 
    if f'{object_class}_material_dict.json' in os.listdir(folder):
        load_dict()
        print(f'material dictionary found, {object_class}_material_dict.json loaded')
    else:
        save_dict()
        print(f'material dictionary not found, {object_class}_material_dict.json created and saved')

    # load first image filename_text and fileclass_text
    current_image = 0
    load_image()
    save_dict()
    count_class()

def load_image():
    # load image included in open_file function`
    global image
    global current_image 
    global image_path
    image_path = folder_path + '/' + image_dict[current_image]
    MAX_SIZE = (400, 400)
    image = Image.open(image_path)
    image.thumbnail(MAX_SIZE)
    image = ImageTk.PhotoImage(image)
    image_label = tk.Label(image=image)
    image_label.image = Image
    image_label.grid(column=0, columnspan=5, row=1, rowspan=3)

    number['text'] = f'{int(current_image+1)} / {len(list_images)} '

    #change filename_text
    filename_text['text'] = image_dict[current_image]

    #change fileclass_text
    for i in material_dict:
        if image_path in material_dict[i]:
            fileclass_text['text'] = i
            return
        else:
            fileclass_text['text'] = 'Not Yet Classified'
    count_class()

def next_image():
    # going to next image
    global image
    global current_image
    global image_path
    if current_image < (len(list_images)-1):
        current_image += 1
        load_image()
    save_dict()

def prev_image():
    # going to previous image
    global image
    global current_image
    global image_path
    if current_image >= 1:
        current_image -= 1
        load_image()
    save_dict()

def select_material(material):
    global material_dict
    # gate
    in_dict = False
    # check if image_path already in the dictionary
    for i in material_dict:
        if image_path in material_dict[i]:
            print(f'object already classified as {i}')
            in_dict = True
            return
    if in_dict == False:
        if image_path not in material_dict[material]:
            material_dict[material].append(image_path)
            print(f'object classified as {material}')
            save_dict()
            count_class()
    for i in material_dict:
        if image_path in material_dict[i]:
            fileclass_text['text'] = i
            save_dict()
            count_class()
            next_image()
            return
        else:
            fileclass_text['text'] = 'Not Yet Classified'
    save_dict()
    count_class()
    next_image()
    

def delete_material_class():
    for i in material_dict:
        if image_path in material_dict[i]:
            material_dict[i].remove(image_path)
            print('object class has been reset')
            fileclass_text['text'] = 'Not Yet Classified'
            save_dict()
            count_class()
            return
    print('object not classified')     
    save_dict()
    count_class()

# have a look at material_dict
def display_dict():
    print(material_dict)
    for i in material_dict:
        print(i, len(material_dict[i]))

# Wipe Dict clean
def wipe_dict():
    global material_dict
    material_dict = {
        'Plastic' : [],
        'Metal' : [],
        'Styrofoam' : [],
        'Glass' : [],
        'Paper' : [],
        'Unknown' : []
    }
    fileclass_text['text'] = 'Not Yet Classified'
    save_dict()
    count_class()
    print('material_dict has been returned to clean slate')

# counting classified images
def count_class():
    global count
    count = 0
    for i in material_dict:
        count += len(material_dict[i])
    classified['text'] = f'{count} / {len(list_images)}'

# save dictionary
def save_dict():
    global material_dict
    with open((folder_path + '/' + object_class + '_' + 'material_dict' + '.json') , 'w') as f:
        json.dump(material_dict,f)

# load dictionary
def load_dict():
    global material_dict
    with open((folder_path + '/' + object_class + '_' + 'material_dict' + '.json') , 'r') as f:
        material_dict = json.load(f)

# after classifying images create individual materials folder and files from dictionary to folder
def copy_files():
    for i in material_dict:
        if f'{object_class}_{i}' in os.listdir(prediction_folder):
            shutil.rmtree(f'{prediction_folder}/{object_class}_{i}')
            print(f"{i}'s original directory has be deleted")
        if len(material_dict[i]) != 0:
            os.makedirs((f'{prediction_folder}/{object_class}_{i}'),exist_ok=True)
            print(f"{i}'s has been created")
            for file in material_dict[i]:
                shutil.copy(file,f'{prediction_folder}/{object_class}_{i}')

# test command (testing)

def test(event):
    print('works')
    print(object_menu.get())


# Keybind Functions -~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~

def handle_keypress(event):
    # handling keypresses for material selection
    if event.char == "1":
        print("1 pressed")
        select_material('Plastic')
    elif event.char == "2":
        print("2 pressed")
        select_material('Metal')
    elif event.char == "3":
        print("3 pressed")    
        select_material('Styrofoam')
    elif event.char == "4":
        print("4 pressed")    
        select_material('Glass')
    elif event.char == "5":
        print("5 pressed")    
        select_material('Paper')
    elif event.char == "6":
        print("6 pressed")    
        select_material('Unknown')
    elif event.char == "o":
        print("o pressed")    
        open_file()

def left(event):
    print("< pressed")    
    prev_image()

def right(event):
    print("> pressed")    
    next_image()

def deldel(event):
    print('del pressed')
    delete_material_class()

def deldelclean(event):
    print('shift del/bksp pressed')
    wipe_dict()

def quitquit(event):
    root.destroy()

# GUI application starts here -~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~

# start
root = tk.Tk()
root.title('Object Material Filter V2.0')
# KeyBinding Controls

root.bind("<Key>", handle_keypress)
root.bind("<Left>", left)
root.bind('<Right>', right)
root.bind('<Escape>', quitquit)
root.bind('<BackSpace>', deldel)
root.bind('<Shift-BackSpace>', deldelclean)
root.bind('<Delete>', deldel)
root.bind('<Shift-Delete>', deldelclean)

# Testing Object Menu
object_menu = StringVar()
object_menu.set('') # default value
w = OptionMenu(root, object_menu, *list_dir, command=test)
w.grid(column=0,row=0)

# Setting Canvas
canvas = tk.Canvas(root, width=700, height=700)
canvas.grid(columnspan=8, rowspan=7)

# instructions
instructions = tk.Label(root, text=f'Please select the what material the {object_class} is made of')
instructions.grid(columnspan=4, column=1, row=0)

number = tk.Label(root, text='Number of Images')
number.grid(columnspan=1, column=3, row=4)

filename_title = tk.Label(root, text='File Name:')
filename_title.grid(columnspan=1, column=0, row=4)

filename_text = tk.Label(root, text='File Name')
filename_text.grid(columnspan=2, column=1, row=4)

fileclass_title = tk.Label(root, text='Object Class:')
fileclass_title.grid(columnspan=1, column=0, row=5)

fileclass_text = tk.Label(root, text='Object Class')
fileclass_text.grid(columnspan=2, column=1, row=5)

classified = tk.Label(root, text='Number Classified')
classified.grid(columnspan=1, column=3, row=5)

# material buttons
plastic_text = tk.StringVar()
plastic_btn = tk.Button(root, textvariable=plastic_text, command=lambda:select_material('Plastic'))
plastic_text.set('Plastic (1)')
plastic_btn.grid(column=0, row=6)

metal_text = tk.StringVar()
metal_btn = tk.Button(root, textvariable=metal_text, command=lambda:select_material('Metal'))
metal_text.set('Metal (2)')
metal_btn.grid(column=1, row=6)

styro_text = tk.StringVar()
styro_btn = tk.Button(root, textvariable=styro_text, command=lambda:select_material('Styrofoam'))
styro_text.set('Styrofoam (3)')
styro_btn.grid(column=2, row=6)

glass_text = tk.StringVar()
glass_btn = tk.Button(root, textvariable=glass_text, command=lambda:select_material('Glass'))
glass_text.set('Glass (4)')
glass_btn.grid(column=3, row=6)

paper_text = tk.StringVar()
paper_btn = tk.Button(root, textvariable=paper_text, command=lambda:select_material('Paper'))
paper_text.set('Paper (5)')
paper_btn.grid(column=4, row=6)

unknown_text = tk.StringVar()
unknown_btn = tk.Button(root, textvariable=unknown_text, command=lambda:select_material('Unknown'))
unknown_text.set('Unknown (6)')
unknown_btn.grid(column=5, row=6)

# function buttons

func0_text = tk.StringVar()
func0_btn = tk.Button(root, textvariable=func0_text, command=lambda:open_directory())
func0_text.set('Root Directory')
func0_btn.grid(column=5, row=0)

func1_text = tk.StringVar()
func1_btn = tk.Button(root, textvariable=func1_text, command=lambda:open_file())
func1_text.set('Open Folder (O)')
func1_btn.grid(column=5, row=1)

func2_text = tk.StringVar()
func2_btn = tk.Button(root, textvariable=func2_text, command=lambda:delete_material_class())
func2_text.set('Delete (del/bksp)')
func2_btn.grid(column=5, row=2)

func3_text = tk.StringVar()
func3_btn = tk.Button(root, textvariable=func3_text, command=lambda:next_image())
func3_text.set('Next + (>)')
func3_btn.grid(column=5, row=3)

func4_text = tk.StringVar()
func4_btn = tk.Button(root, textvariable=func4_text, command=lambda:prev_image())
func4_text.set('Prev - (<)')
func4_btn.grid(column=5, row=4)

func5_text = tk.StringVar()
func5_btn = tk.Button(root, textvariable=func5_text, command=lambda:copy_files())
func5_text.set('Copy Files')
func5_btn.grid(column=5, row=5)

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
root.mainloop()

# Comments-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~

# By Jlee

# Version 1.0 02/05/2021
 # - finished first complete interation

# Version 1.1-2 02/05/2021
 # - (done) added more function buttons for backup
 # - (done) want to add function to extract multiple files at once and change directories to different objects so that when one object class material classification is complete the next folder can be selected without moving screens(plus use of hotkeys)
 # - find images that have not been classified quickly
 # - 