from tkinter import *
from PIL import ImageTk, Image
import tkinter as tk
import os
import json
import shutil

def filter_app(pathpath_in,window):
    global material_dict 
    global stats_dict
    global list_dir
    global object_list
    global object_class
    global object_menu
    global pathpath

# Variables -~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~

    # for main_gui functionality
    pathpath = pathpath_in
    
    # dict for materials lists for record and use when moving files
    material_dict = {
        'Plastic' : [],
        'Metal' : [],
        'Styrofoam' : [],
        'Glass' : [],
        'Paper' : [],
        'Unknown' : [],
        'FaceMask' : [],
        'TetraPack' : []
    }

    list_dir = ['']

    object_list = ['bottle', 'can', 'cup', 'box_drink', 'face_mask', 'plastic_bag']
    object_class = '_______'
    
    # dict for recording classified object materials for stat tracking
    stats_dict = {}
    for i in object_list:
        stats_dict[i] = material_dict
    
    # Functions -~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~

    # Read all folders in the selected Directory
    def open_directory():
        try:
            global root_dir
            global list_dir
            global root_path
            global dir_dict
            global prediction_folder
            global dir_index
            root_dir = pathpath
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
                # display the amount of images in a folder and add object_class to OptionMenu
                num_img = len([ i for i in os.listdir(dir_dict[i]) if '.jpg' in i])
                w['menu'].add_command(label=f'{i} ({num_img})', command=tk._setit(object_menu, f'{i} ({num_img})', change_folder))
            
            # setting the first num_img need it's own variable 
            dir_index = 0
            num_img_init = len([ i for i in os.listdir(dir_dict[list_dir[dir_index]]) if '.jpg' in i])
            object_menu.set(f'{list_dir[0]} ({num_img_init})')
            open_file_multi(dir_dict[list_dir[dir_index]])
        except FileNotFoundError:
            print('Directory Not Selected (Open Folder)')

    def change_folder(event):
        global object_menu
        global list_dir
        global dir_dict
        global dir_index
        # need to split() the object_menu.get() get just the object name without the num_img
        temp_object = object_menu.get().split()[0]
        dir_index = list_dir.index(temp_object)
        open_file_multi(dir_dict[list_dir[dir_index]])
        copy_files()

    def up_menu():
        try:
            global dir_index
            if dir_index >= 1:
                dir_index -= 1
                num_img_init = len([ i for i in os.listdir(dir_dict[list_dir[dir_index]]) if '.jpg' in i])
                object_menu.set(f'{list_dir[dir_index]} ({num_img_init})')
                open_file_multi(dir_dict[list_dir[dir_index]])
            else:
                print('Top of Options Menu')
        except NameError:
            pass

    def down_menu():
        try:
            global dir_index
            if dir_index < (len(list_dir))-1:
                dir_index += 1
                num_img_init = len([ i for i in os.listdir(dir_dict[list_dir[dir_index]]) if '.jpg' in i])
                object_menu.set(f'{list_dir[dir_index]} ({num_img_init})')  
                open_file_multi(dir_dict[list_dir[dir_index]])
            else:
                print('Bottom of Options Menu')
        except NameError:
            pass

    def open_file_multi(dir_path):
        #using global to create a global variable
        global list_images
        global image_dict
        global folder_path
        global current_image
        global folder
        global object_class
        global material_dict
        global object_class
        global image_label

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
        print(f'{len(list_images)} image(s) in this folder(list)')
        material_dict = {
            'Plastic' : [],
            'Metal' : [],
            'Styrofoam' : [],
            'Glass' : [],
            'Paper' : [],
            'Unknown' : [],
            'FaceMask' : [],
            'TetraPack' : []
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
        try:
            load_image()
            print('There are images in the folder')
            count_class()
        except KeyError:
            image_label.config(image='')
            filename_text['text'] = 'File Name'
            fileclass_text['text'] = 'Material'
            number_img['text'] = 'None'
            classified['text'] = 'None'
            print(f'No images in {object_class}')
        copy_files()

    def load_image():
        # load image included in open_file function`
        global image
        global current_image 
        global image_path
        global image_label
        image_path = f'{folder_path}/{image_dict[current_image]}'
        MAX_SIZE = (300, 300)
        image = Image.open(image_path)
        image.thumbnail(MAX_SIZE)
        image = ImageTk.PhotoImage(image)
        image_label = tk.Label(root, image=image)
        image_label.image = Image
        image_label.grid(column=0, columnspan=5, row=1, rowspan=3)

        number_img['text'] = f'{int(current_image+1)} / {len(list_images)}'

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
        copy_files()

    def next_image():
        try:
            # going to next image
            global image
            global current_image
            global image_path
            if current_image < (len(list_images)-1):
                current_image += 1
                load_image()
            else:
                print('Last Image')
            save_dict()
            copy_files()
        except NameError:
            pass

    def prev_image():
        try:
            # going to previous image
            global image
            global current_image
            global image_path
            if current_image >= 1:
                current_image -= 1
                load_image()
            else:
                print('First Image')
            save_dict()
        except NameError:
            pass

    def select_material(material):
        try:
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
                    copy_files()
                    return
                else:
                    fileclass_text['text'] = 'Not Yet Classified'
            save_dict()
            count_class()
            next_image()
            copy_files()
        except NameError:
            pass

    def skip_select_material(material):
        global material_dict
        global image_dict
        global folder_path
        try:
            wipe_dict(2)
            for i in range(len(image_dict)):
                material_dict[material].append(f'{folder_path}/{image_dict[i]}')
            if image_path in material_dict[material]:
                    fileclass_text['text'] = material
            print(f'All {object_class}(s) have been classified as {material}')
            save_dict()
            count_class()
            copy_files()
        except NameError:
            pass

    def delete_material_class():
        try:
            for i in material_dict:
                if image_path in material_dict[i]:
                    material_dict[i].remove(image_path)
                    print('object class has been reset')
                    fileclass_text['text'] = 'Not Yet Classified'
                    save_dict()
                    count_class()
                    copy_files()
                    return
            print('object not classified')     
            save_dict()
            count_class()
            copy_files()
        except NameError:
            pass

    # Wipe Dict clean
    def wipe_dict(type_):
        global material_dict
        # for shift-del/bksp
        if type_ == 1:
            load_dict()
            material_dict = {
                'Plastic' : [],
                'Metal' : [],
                'Styrofoam' : [],
                'Glass' : [],
                'Paper' : [],
                'Unknown' : [],
                'FaceMask' : [],
                'TetraPack' : []
            }
            fileclass_text['text'] = 'Not Yet Classified'
            save_dict()
            count_class()
            copy_files()
            print('material_dict has been returned to clean slate')
        # for skip_select_material
        if type_ == 2:
            load_dict()
            material_dict = {
                'Plastic' : [],
                'Metal' : [],
                'Styrofoam' : [],
                'Glass' : [],
                'Paper' : [],
                'Unknown' : [],
                'FaceMask' : [],
                'TetraPack' : []
            }
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
        with open(f'{folder_path}/{object_class}_material_dict.json' , 'w') as f:
            json.dump(material_dict,f)

    # load dictionary
    def load_dict():
        global material_dict
        with open(f'{folder_path}/{object_class}_material_dict.json' , 'r') as f:
            material_dict = json.load(f)

    # after classifying images create individual materials folder and files from dictionary to folder
    def copy_files():
        try:
            global stats_dict
            global material_dict
            # create folder to hold all classified object materials
            os.makedirs((f'{prediction_folder}/Object Materials'), exist_ok=True)
            try:
                with open(f'{prediction_folder}/Object Materials/stats.json', 'r') as f:
                    stats_dict = json.load(f)
                print('stats.json loaded')
            except:
                print("No stats.json")
            
            stats_dict[object_class] = material_dict

            # create and update stats dict
            with open(f'{prediction_folder}/Object Materials/stats.json', 'w') as f:
                json.dump(stats_dict,f)

            for i in material_dict:
                if f'{object_class}_{i}' in os.listdir(f'{prediction_folder}/Object Materials'):
                    shutil.rmtree(f'{prediction_folder}/Object Materials/{object_class}_{i}')
                    print(f"{i}'s original directory has be deleted")
                if len(material_dict[i]) != 0:
                    os.makedirs(f'{prediction_folder}/Object Materials/{object_class}_{i}',exist_ok=True)
                    print(f"{i}'s has been created")
                    for file in material_dict[i]:
                        shutil.copy(file,f'{prediction_folder}/Object Materials/{object_class}_{i}')
        except NameError:
            print('Directory Not Selected (Copy Files)')

    # Keybind Functions -~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~

    def handle_keypress(event):
        # handling keypresses for material selection
        if event.char == "1":
            print("1 pressed")
            try:
                select_material('Plastic')
            except NameError:
                pass
        elif event.char == "2":
            print("2 pressed")
            try:
                select_material('Metal')
            except NameError:
                pass
        elif event.char == "3":
            print("3 pressed")   
            try: 
                select_material('Styrofoam')
            except NameError:
                pass
        elif event.char == "4":
            print("4 pressed")    
            try:
                select_material('Glass')
            except NameError:
                pass
        elif event.char == "5":
            print("5 pressed")    
            try:
                select_material('Paper')
            except NameError:
                pass
        elif event.char == "6":
            print("6 pressed")    
            try:
                select_material('Unknown')
            except NameError:
                pass

    def left(event):
        print("< pressed")    
        try:
            prev_image()
        except NameError:
            pass

    def right(event):
        print("> pressed")    
        try:
            next_image()
        except NameError:
            pass

    def up(event):
        print('/\ pressed')
        up_menu()

    def down(event):
        print('\/ pressed')
        down_menu()

    def deldel(event):
        print('del pressed')
        try:
            delete_material_class()
        except NameError:
            pass

    def deldelclean(event):
        print('shift del/bksp pressed')
        try:
            wipe_dict(1)
        except NameError:
            pass

    def quitquit(event):
        root.destroy()

    # GUI application starts here -~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~

    # Starts
    root = tk.Toplevel(window)
    root.geometry('700x720')
    root.title('Object Material Filter')

    # KeyBinding Controls
    root.bind("<Key>", handle_keypress)
    root.bind("<Left>", left)
    root.bind('<Right>', right)
    root.bind('<Escape>', quitquit)
    root.bind('<BackSpace>', deldel)
    root.bind('<Shift-BackSpace>', deldelclean)
    root.bind('<Delete>', deldel)
    root.bind('<Shift-Delete>', deldelclean)
    root.bind('<Up>', up)
    root.bind('<Down>', down)

    # Testing Object Menu
    object_menu = StringVar()
    object_menu.set('None') # default value
    w = OptionMenu(root, object_menu, None)
    w.config(width=12, height=3)
    w.grid(column=5, row=0, sticky='w')

    # Setting Canvas
    canvas = tk.Canvas(root, width=700, height=700)
    canvas.grid(columnspan=8, rowspan=7)

    # Instructions
    instructions = tk.Label(root, text=f'Please select the what material the {object_class} is made of', font=('', 12, 'bold'))
    instructions.grid(columnspan=5, column=0, row=0)

    filename_title = tk.Label(root, text='File Name:', font=('', 12))
    filename_title.grid(columnspan=1, column=0, row=4)

    filename_text = tk.Label(root, text='File Name', font=('', 12))
    filename_text.grid(columnspan=2, column=1, row=4)

    fileclass_title = tk.Label(root, text='Material:', font=('', 12))
    fileclass_title.grid(columnspan=1, column=0, row=5)

    fileclass_text = tk.Label(root, text='Material', font=('', 12))
    fileclass_text.grid(columnspan=2, column=1, row=5)

    number_img = tk.Label(root, text='None', font=('', 12))
    number_img.grid(columnspan=1, column=3, row=4)

    classified = tk.Label(root, text='None', font=('', 12))
    classified.grid(columnspan=1, column=3, row=5)

    # material buttons
    plastic_text = tk.StringVar()
    plastic_btn = tk.Button(root, textvariable=plastic_text, command=lambda:select_material('Plastic'), height=3, width=15)
    plastic_text.set('Plastic (1)')
    plastic_btn.grid(column=0, row=6)

    metal_text = tk.StringVar()
    metal_btn = tk.Button(root, textvariable=metal_text, command=lambda:select_material('Metal'), height=3, width=15)
    metal_text.set('Metal (2)')
    metal_btn.grid(column=1, row=6)

    styro_text = tk.StringVar()
    styro_btn = tk.Button(root, textvariable=styro_text, command=lambda:select_material('Styrofoam'), height=3, width=15)
    styro_text.set('Styrofoam (3)')
    styro_btn.grid(column=2, row=6)

    glass_text = tk.StringVar()
    glass_btn = tk.Button(root, textvariable=glass_text, command=lambda:select_material('Glass'), height=3, width=15)
    glass_text.set('Glass (4)')
    glass_btn.grid(column=3, row=6)

    paper_text = tk.StringVar()
    paper_btn = tk.Button(root, textvariable=paper_text, command=lambda:select_material('Paper'), height=3, width=15)
    paper_text.set('Paper (5)')
    paper_btn.grid(column=4, row=6)

    unknown_text = tk.StringVar()
    unknown_btn = tk.Button(root, textvariable=unknown_text, command=lambda:select_material('Unknown'), height=3, width=15)
    unknown_text.set('Unknown (6)')
    unknown_btn.grid(column=5, row=6, sticky='w')

    facemask_text = tk.StringVar()
    facemask_btn = tk.Button(root, textvariable=facemask_text, command=lambda:skip_select_material('FaceMask'), height=3, width=15)
    facemask_text.set('Face Masks')
    facemask_btn.grid(column=0, row=7, sticky='n')

    plasbag_text = tk.StringVar()
    plasbag_btn = tk.Button(root, textvariable=plasbag_text, command=lambda:skip_select_material('Plastic'), height=3, width=15)
    plasbag_text.set('Plastic Bags')
    plasbag_btn.grid(column=1, row=7, sticky='n')

    tetra_text = tk.StringVar()
    tetra_btn = tk.Button(root, textvariable=tetra_text, command=lambda:skip_select_material('TetraPack'), height=3, width=15)
    tetra_text.set('Box Drinks')
    tetra_btn.grid(column=2, row=7, sticky='n')

    # function buttons

    func2_text = tk.StringVar()
    func2_btn = tk.Button(root, textvariable=func2_text, command=lambda:delete_material_class(), height=4, width=15)
    func2_text.set('Delete (del/bksp)')
    func2_btn.grid(column=5, row=2, sticky='w')

    func3_text = tk.StringVar()
    func3_btn = tk.Button(root, textvariable=func3_text, command=lambda:next_image(), height=4, width=15)
    func3_text.set('Next + (>)')
    func3_btn.grid(column=5, row=3, sticky='w')

    func4_text = tk.StringVar()
    func4_btn = tk.Button(root, textvariable=func4_text, command=lambda:prev_image(), height=4, width=15)
    func4_text.set('Prev - (<)')
    func4_btn.grid(column=5, row=4, sticky='w')
    
    open_directory()
    # finish
    root.mainloop()

# Comments-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~

# By Jlee

# Version 1.0 02/05/2021
 # - finished first complete interation

# Version 1.1-2.3 02/05/2021
 # - (done) added more function buttons for backup
 # - (done) want to add function to extract multiple files at once and change directories to different objects so that when one object class material classification is complete the next folder can be selected without moving screens(plus use of hotkeys)
 # - (done) added up and down arrow keybinds to change object_class
 # - (done) added skip_select_material for face masks/ plastic bags/ box drinks
 # - (done) added Option Menu (object selection)
 # - (to be added) find images that have not been classified quickly
 # - (done) try and except added to clear avoidable errors

 #reupload 05052021