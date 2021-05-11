from tkinter import *
from PIL import ImageTk,Image 
import tkinter as tk
import os
import json
import shutil
from main_function.main_image_bound import img_bound

def correct_check(project, name, window):
    global correct_dict, Project, Name

    Project = project
    Name = name

    #Variables -~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    correct_dict = {
        "Correct" : [],
        "Incorrect" : [],
        "Remove" : [],
    }

    def open_file():
        #using global to create a global variable
        global list_images
        global image_dict
        global folder_path
        global current_image
        global image640
        global labels_path
        
        image640_path = f'{Project}/images'
        labels_path = f'{Project}{Name}/labels'
        
        list_images = sorted(os.listdir(image640_path)) 
        list_images = [i for i in list_images if '.jpg' in i] # names of images into a list
        os.chdir(image640_path)
        folder_path = os.getcwd()

        image_dict = {}
        for i in range(len(list_images)):
            image_dict[i] = list_images[i]
        print(f'{len(list_images)} images in this folder')
        
        # load material_dict if in folder (continue to work if work has already been done)
        if 'correct_dict.json' in os.listdir(image640_path):
            load_dict()
            print('Correct list dictionary found.')
        else:
            print('Correct list dictionary not found.')

        # load first image filename_text and fileclass_text
        current_image = 0
        load_image()
        count_class()

    def load_image():
        # load image included in open_file function`
        global image
        global current_image 
        global image_path
        global image_ori, image_bou

        #Grab Screen Height and Width
        screen_width = root.winfo_screenwidth() * 0.4
        screen_height = root.winfo_screenheight() * 0.4
        MAX_SIZE = (screen_width, screen_height)

        # for original image
        image_path = f'{folder_path}/{image_dict[current_image]}'
        image = Image.open(image_path)
        image.thumbnail(MAX_SIZE)
        image_ = ImageTk.PhotoImage(image)
        image_ori = tk.Label(left_frame, image=image_)
        image_ori.image = image_
        image_ori.grid(column=0, columnspan=5, row=0, rowspan=1)

        # for bounded image
        try:
            bou_img = img_bound(image640_path, labels_path,  image_dict[current_image].split('.')[0])
            bou_img = Image.fromarray(bou_img)
            b, g, r = bou_img.split()
            bou_img = Image.merge('RGB', (r,g,b))
            bou_img.thumbnail(MAX_SIZE)
            bou_img_ = ImageTk.PhotoImage(bou_img)
            image_bou = tk.Label(left_frame, image=bou_img_)
            image_bou.image = bou_img_
            image_bou.grid(column=0, columnspan=5, row=5, rowspan=1)
        except:
            if AttributeError or UnboundLocalError:
                image_bou = tk.Label(left_frame, text='No Bounded Image')
                image_bou.grid(column=0, columnspan=5, row=5, rowspan=3)

        number['text'] = f'{int(current_image+1)} / {len(list_images)} '

        #change filename_text
        filename_text['text'] = image_dict[current_image]

        #change fileclass_text
        for i in correct_dict:
            if image_path in correct_dict[i]:
                fileclass_text['text'] = i
                return
            else:
                fileclass_text['text'] = 'Not Yet Classified'
        count_class()

    # counting classified images
    def count_class():
        global count
        count = 0
        for i in correct_dict:
            count += len(correct_dict[i])
        classified['text'] = f'{count} / {len(list_images)}'

    def next_image():
        # going to next image
        global image
        global current_image
        global image_path
        if current_image < (len(list_images)-1):
            current_image += 1.0
            image_ori.destroy()
            image_bou.destroy()
            load_image()
        save_dict()

    def delete_label_class():
        for i in correct_dict:
            if image_path in correct_dict[i]:
                correct_dict[i].remove(image_path)
                print('object class has been reset')
                fileclass_text['text'] = 'Not Yet Classified'
                save_dict()
                count_class()
                return
        print('object not classified')     
        save_dict()
        count_class()

    def prev_image():
        # going to previous image
        global image
        global current_image
        global image_path
        if current_image >= 1:
            current_image -= 1
            image_bou.destroy()
            image_ori.destroy()
            load_image()
        save_dict()

    # save dictionary
    def save_dict():
        global correct_dict
        with open(f'{folder_path}/correct_dict.json' , 'w') as f:
            json.dump(correct_dict,f)

    def load_dict():
        global correct_dict
        with open(f'{folder_path}/correct_dict.json' , 'r') as f:
            correct_dict = json.load(f)


    def select_label(correct):
        global correct_dict
        # gate
        in_dict = False
        # check if image_path already in the dictionary
        for i in correct_dict:
            if image_path in correct_dict[i]:
                print(f'Image already classified as {i}')
                in_dict = True
        if in_dict == False:
            if image_path not in correct_dict[correct]:
                correct_dict[correct].append(image_path)
                print(f'Image classified as {correct}')
                save_dict()
                count_class()
        for i in correct_dict:
            if image_path in correct_dict[i]:
                fileclass_text['text'] = i
                next_image()
                save_dict()
                count_class()
                return
            else:
                fileclass_text['text'] = 'Not Yet Classified'
        next_image()
        save_dict()
        count_class()


    def delete_label_class():
        for i in correct_dict:
            if image_path in correct_dict[i]:
                correct_dict[i].remove(image_path)
                print('object class has been reset')
                fileclass_text['text'] = 'Not Yet Classified'
                save_dict()
                count_class()
                return
        print('object not classified')     
        save_dict()
        count_class()

    def wipe_dict(event):
        global correct_dict
        correct_dict = {
            'Correct' : [],
            'Incorrect' : [],
            'Remove' : [],
        }
        save_dict()
        count_class()
        print('correct_dict has been returned to clean slate')

    def copy_files():
        global folder_path
        os.chdir(Project + Name)

        # remove folders
        try:
            if 'Correct' and 'Incorrect' and 'Remove' in os.listdir(os.getcwd()):
                shutil.rmtree('./Correct/')
                shutil.rmtree('./Incorrect/')
                shutil.rmtree('./Remove/')
                print('labeled folders deleted')
        except:
            print('labeled folders not found')

        # create folders
        os.makedirs("./Correct/",exist_ok=True)
        os.makedirs("./Correct/images",exist_ok=True)
        os.makedirs("./Correct/labels",exist_ok=True)
        os.makedirs("./Incorrect/",exist_ok=True)
        os.makedirs("./Incorrect/images",exist_ok=True)
        os.makedirs("./Incorrect/labels",exist_ok=True)
        os.makedirs("./Remove/",exist_ok=True)
        os.makedirs("./Remove/images",exist_ok=True)
        os.makedirs("./Remove/labels",exist_ok=True)
        print('labeled folders created')

        for file in correct_dict["Correct"]:
            try:
                file_name = file.split("/")[-1]
                shutil.copy(f'{Project}/fullsize_images/{file_name}', f'{Project}{Name}/Correct/images/{file_name}')
                shutil.copy(f'{Project}{Name}/labels/{file_name[:-4]}.txt', f'{Project}{Name}/Correct/labels/{file_name[:-4]}.txt')
            except FileNotFoundError:
                print(f'Label for {file_name} not found!')
        for file in correct_dict["Incorrect"]:
            try:
                file_name = file.split("/")[-1]
                shutil.copy(f'{Project}/fullsize_images/{file_name}', f'{Project}{Name}/Incorrect/images/{file_name}')
                shutil.copy(f'{Project}{Name}/labels/{file_name[:-4]}.txt', f'{Project}{Name}/Incorrect/labels/{file_name[:-4]}.txt')
            except FileNotFoundError:
                print(f'Label for {file_name} not found!')
        for file in correct_dict["Remove"]:
            try:
                file_name = file.split("/")[-1]
                shutil.copy(f'{Project}/fullsize_images/{file_name}', f'{Project}{Name}/Remove/images/{file_name}')
                shutil.copy(f'{Project}{Name}/labels/{file_name[:-4]}.txt', f'{Project}{Name}/Remove/labels/{file_name[:-4]}.txt')
            except FileNotFoundError:
                print(f'Label for {file_name} not found!')
        root.update()
        root.quit()
        root.destroy()


    # Keybind Functions

    def handle_keypress(event):
        # handling keypresses for material selection
        if event.char == "1":
            print("1 pressed")
            select_label('Correct')
        elif event.char == "2":
            print("2 pressed")
            select_label('Incorrect')
        elif event.char == "3":
            print("3 pressed")
            select_label('Remove')
        elif event.char == "o":
            print("o pressed")
            open_file()


    def left(event):
        print("< pressed")    
        prev_image()

    def right(event):
        print("> pressed")    
        next_image()

    def quitquit(event):
        root.destroy()

    def deldel(event):
        print('del pressed')
        delete_label_class()
    # GUI application starts here -~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~

    # start
    # start
    root = tk.Toplevel(window)
    root.title("YOLO Image Reviewer")

    left_frame = Frame(root)
    left_frame.grid(row=0, column=0, sticky="nswe")

    right_frame = Frame(root)
    right_frame.grid(row=0, column=1, sticky="nswe")

    # KeyBinding Controls

    root.bind("<Key>", handle_keypress)
    root.bind("<Left>", left)
    root.bind('<Right>', right)
    root.bind('<Escape>', quitquit)
    root.bind('<BackSpace>', deldel)
    root.bind('<Delete>', deldel)
    root.bind('<Shift-BackSpace>', wipe_dict)
    root.bind('<Shift-Delete>', wipe_dict)

    canvas = tk.Canvas(root, width=1400, height=700)
    canvas.grid(columnspan=12, rowspan=7)

    func0_text = tk.StringVar()
    func0_btn = tk.Button(right_frame, textvariable=func0_text, width = 31, height = 4, command=lambda:copy_files())
    func0_text.set('Copy Files and Quit')
    func0_btn.grid(column=6, row=16, columnspan=2,sticky="w")

    func2_text = tk.StringVar()
    func2_btn = tk.Button(right_frame, textvariable=func2_text, width =15, height = 4,command=lambda:delete_label_class())
    func2_text.set('Delete (del)')
    func2_btn.grid(column=7, row=5,sticky="w")

    func3_text = tk.StringVar()
    func3_btn = tk.Button(right_frame, textvariable=func3_text, width = 15, height = 4,command=lambda:next_image())
    func3_text.set('Next + (>)')
    func3_btn.grid(column=7, row=7,sticky="w")

    func4_text = tk.StringVar()
    func4_btn = tk.Button(right_frame, textvariable=func4_text, width = 15, height = 4,command=lambda:prev_image())
    func4_text.set('Prev - (<)')
    func4_btn.grid(column=7, row=9,sticky="w")


    number = tk.Label(right_frame, text='',font=('Calibri', 20))
    number.grid(columnspan=1, column=8, row=1)

    classified = tk.Label(right_frame, text='',font=('Calibri', 20))
    classified.grid(columnspan=1, column=8, row=2)

    filename_title = tk.Label(right_frame, text='File Name:',font=('Calibri', 20))
    filename_title.grid(columnspan=1, column=6, row=1,sticky="w")

    filename_text = tk.Label(right_frame, text='File Name',font=('Calibri', 20))
    filename_text.grid(columnspan=1, column=7, row=1,sticky="w")

    filename_title = tk.Label(right_frame, text='Label:',font=('Calibri', 20))
    filename_title.grid(columnspan=1, column=6, row=2,sticky="w")

    fileclass_text = tk.Label(right_frame, text='Correct/Incorrect/Remove',font=('Calibri', 20))
    fileclass_text.grid(columnspan=1, column=7, row=2,sticky="w")

    # labelling buttons
    correct_txt = tk.StringVar()
    correct_btn = tk.Button(right_frame, textvariable=correct_txt, height=4, width = 15,command=lambda:select_label('Correct'))
    correct_txt.set('Correct (1)')
    correct_btn.grid(column=6, row=5)

    incorrect_txt = tk.StringVar()
    incorrect_btn = tk.Button(right_frame, textvariable=incorrect_txt, height =4, width = 15, command=lambda:select_label('Incorrect'))
    incorrect_txt.set('Incorrect (2)')
    incorrect_btn.grid(column=6, row=7)

    remove_txt = tk.StringVar()
    remove_btn = tk.Button(right_frame, textvariable=remove_txt, height=4, width = 15,command=lambda:select_label('Remove'))
    remove_txt.set('Remove (3)')
    remove_btn.grid(column=6, row=9)

    open_file()

    root.mainloop()
#Coded by A.Lam with reference to J.Lee
