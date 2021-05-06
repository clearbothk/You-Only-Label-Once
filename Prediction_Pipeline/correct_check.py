from tkinter import filedialog
from tkinter import *
from PIL import ImageTk,Image 
import tkinter as tk
import os
import glob
from time import localtime, strftime
import json
import shutil


def correct_check():
    global correct_dict
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
        global original
        global base

        # clicking button allows user to select specific directory
        original = filedialog.askdirectory() 
        folder = original + '/bounded_images/'
        base = original[:-17]

        list_images = sorted(os.listdir(folder)) 
        list_images = [i for i in list_images if '.jpg' in i] # names of images into a list
        os.chdir(folder)
        folder_path = os.getcwd()
        print(folder_path)

        image_dict = {}
        for i in range(len(list_images)):
            image_dict[i] = list_images[i]
        print(f'{len(list_images)} images in this folder')
        
        # load material_dict if in folder (continue to work if work has already been done)
        if 'correct_dict.json' in os.listdir(folder):
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
        image_path = folder_path + '/' + image_dict[current_image]
        image = Image.open(image_path)
        MAX_SIZE = (640, 640)
        image.thumbnail(MAX_SIZE)
        image = ImageTk.PhotoImage(image)
        image_label = tk.Label(image=image)
        image_label.image = Image
        image_label.grid(column=0, columnspan=5, row=1, rowspan=3)

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
            load_image()
        save_dict()

    # save dictionary
    def save_dict():
        global correct_dict
        with open((folder_path + '/' + 'correct_dict' + '.json') , 'w') as f:
            json.dump(correct_dict,f)

    def load_dict():
        global correct_dict
        with open((folder_path + '/' + 'correct_dict' + '.json') , 'r') as f:
            correct_dict = json.load(f)


    def select_label(correct):
        global correct_dict
        # object_class gate

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
        # print(folder_path)
        os.chdir(folder_path)
        os.chdir("..")
        # print(os.getcwd())
        os.makedirs("./Correct/",exist_ok=True)
        os.makedirs("./Correct/images",exist_ok=True)
        os.makedirs("./Correct/labels",exist_ok=True)
        os.makedirs("./Incorrect/",exist_ok=True)
        os.makedirs("./Incorrect/images",exist_ok=True)
        os.makedirs("./Incorrect/labels",exist_ok=True)
        os.makedirs("./Remove/",exist_ok=True)
        os.makedirs("./Remove/images",exist_ok=True)
        os.makedirs("./Remove/labels",exist_ok=True)

        for file in correct_dict["Correct"]:
            try:
                file_name = file.split("/")[-1]
                shutil.copy(f'{base}/fullsize_images/{file_name}', f'{original}/Correct/images/{file_name}')
                shutil.copy(f'{original}/labels/{file_name[:-4]}.txt', f'{original}/Correct/labels/{file_name[:-4]}.txt')
            except FileNotFoundError:
                print(f'Label for {file_name} not found!')
        for file in correct_dict["Incorrect"]:
            try:
                file_name = file.split("/")[-1]
                shutil.copy(f'{base}/fullsize_images/{file_name}', f'{original}/Incorrect/images/{file_name}')
                shutil.copy(f'{original}/labels/{file_name[:-4]}.txt', f'{original}/Incorrect/labels/{file_name[:-4]}.txt')
            except FileNotFoundError:
                print(f'Label for {file_name} not found!')
        for file in correct_dict["Remove"]:
            try:
                file_name = file.split("/")[-1]
                shutil.copy(f'{base}/fullsize_images/{file_name}', f'{original}/Remove/images/{file_name}')
                shutil.copy(f'{original}/labels/{file_name[:-4]}.txt', f'{original}/Remove/labels/{file_name[:-4]}.txt')
            except FileNotFoundError:
                print(f'Label for {file_name} not found!')

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
    root = tk.Tk()
    root.title("YOLO Image Reviewer")

    # KeyBinding Controls

    root.bind("<Key>", handle_keypress)
    root.bind("<Left>", left)
    root.bind('<Right>', right)
    root.bind('<Escape>', quitquit)
    root.bind('<BackSpace>', deldel)
    root.bind('<Delete>', deldel)
    root.bind('<Shift-BackSpace>', wipe_dict)
    root.bind('<Shift-Delete>', wipe_dict)

    canvas = tk.Canvas(root, width=700, height=700)
    canvas.grid(columnspan=7, rowspan=7)

    func0_text = tk.StringVar()
    func0_btn = tk.Button(root, textvariable=func0_text, command=lambda:copy_files())
    func0_text.set('Copy Files')
    func0_btn.grid(column=5, row=5)


    func1_text = tk.StringVar()
    func1_btn = tk.Button(root, textvariable=func1_text, command=lambda:open_file())
    func1_text.set('Open Folder (O)')
    func1_btn.grid(column=5, row=1)

    func2_text = tk.StringVar()
    func2_btn = tk.Button(root, textvariable=func2_text, command=lambda:delete_label_class())
    func2_text.set('Delete (del)')
    func2_btn.grid(column=5, row=2)

    func3_text = tk.StringVar()
    func3_btn = tk.Button(root, textvariable=func3_text, command=lambda:next_image())
    func3_text.set('Next + (>)')
    func3_btn.grid(column=5, row=3)

    func4_text = tk.StringVar()
    func4_btn = tk.Button(root, textvariable=func4_text, command=lambda:prev_image())
    func4_text.set('Prev - (<)')
    func4_btn.grid(column=5, row=4)


    number = tk.Label(root, text='')
    number.grid(columnspan=1, column=3, row=4)

    classified = tk.Label(root, text='')
    classified.grid(columnspan=1, column=3, row=5)

    filename_title = tk.Label(root, text='File Name:')
    filename_title.grid(columnspan=1, column=0, row=4)

    filename_text = tk.Label(root, text='File Name')
    filename_text.grid(columnspan=2, column=1, row=4)

    filename_title = tk.Label(root, text='Label:')
    filename_title.grid(columnspan=1, column=0, row=5)

    fileclass_text = tk.Label(root, text='Correct/Incorrect/Remove')
    fileclass_text.grid(columnspan=2, column=1, row=5)

    # labelling buttons
    correct_txt = tk.StringVar()
    correct_btn = tk.Button(root, textvariable=correct_txt, command=lambda:select_label('Correct'))
    correct_txt.set('Correct (1)')
    correct_btn.grid(column=0, row=6)

    incorrect_txt = tk.StringVar()
    incorrect_btn = tk.Button(root, textvariable=incorrect_txt, command=lambda:select_label('Incorrect'))
    incorrect_txt.set('Incorrect (2)')
    incorrect_btn.grid(column=1, row=6)

    remove_txt = tk.StringVar()
    remove_btn = tk.Button(root, textvariable=remove_txt, command=lambda:select_label('Remove'))
    remove_txt.set('Remove (3)')
    remove_btn.grid(column=3, row=6)

    # finish
    root.mainloop()

#Coded by A.Lam with reference to J.Lee


# from tkinter import filedialog
# from tkinter import *
# from PIL import ImageTk,Image 
# import tkinter as tk
# import os
# import glob
# from time import localtime, strftime
# import shutil

# window = tk.Tk()
# window.title( 'YOLO Image Reviewer' )


# Console = Text(window,width=40, height=8)
# def write(*message, end = "\n", sep = " "):
#     text = ""
#     for item in message:
#         text += "{}".format(item)
#         text += sep
#     text += end
#     Console.insert(INSERT, text)
#     Console.yview(tk.END)

# # Create a photoimage object of the image in the path
# image_list = []
# bounded_image_name = ""
# images = iter(image_list)
# correct_label_list = []
# incorrect_label_list = []
# add_to_correct = True

# def next_img():  
#     try:
#         img = next(images)  # get the next image from the iterator
#         img_file_name = img    
#     except StopIteration:
#         write("No More Images")
#         return  # if there are no more images, do nothing

#     # load the image and display it
#     img = Image.open(img)
#     basewidth = 300
#     wpercent = (basewidth/float(img.size[0]))
#     hsize = int((float(img.size[1])*float(wpercent)))
#     img = img.resize((basewidth,hsize), Image.ANTIALIAS)
#     img = ImageTk.PhotoImage(img)
#     panel.img = img  # keep a reference so it's not garbage collected
#     panel['image'] = img

#     return img_file_name

# def load_images():
#     global image_list
#     global images
#     global bounded_image_name
#     glob_test =  os.listdir()
#     image_list = glob_test
#     write(f"{len(image_list)} Image Loaded!")
#     images = iter(image_list)
#     bounded_image_name = next_img()
#     return glob_test

# def browse_button_IN():
#     # Allow user to select a directory and store it in global var
#     # called folder_path
#     global folder_path_IN
#     filename_IN = filedialog.askdirectory(title='Please Select YOLO Prediction Folder')
#     folder_path_IN.set(filename_IN)
#     os.chdir(filename_IN+"/bounded_images")
#     load_images()


# def save_output():
    
#     time = strftime("%Y%m%d", localtime())
#     # with open(folder_path_OUT_var+f"/{time}_correct_output.txt", "w") as f:
#     #     for line in correct_label_list:
#     #         f.write("%s\n" % line)
#     # with open(folder_path_OUT_var+f"/{time}_incorrect_output.txt", "w") as f:
#     #     for line in incorrect_label_list:
#     #         f.write("%s\n" % line)

#     os.makedirs(folder_path_IN.get()+"/Correct/",exist_ok=True)
#     os.makedirs(folder_path_IN.get()+"/Correct/images",exist_ok=True)
#     os.makedirs(folder_path_IN.get()+"/Correct/labels",exist_ok=True)
#     os.makedirs(folder_path_IN.get()+"/Relabel/",exist_ok=True)
#     os.makedirs(folder_path_IN.get()+"/Relabel/images",exist_ok=True)
#     os.makedirs(folder_path_IN.get()+"/Relabel/labels",exist_ok=True)

#     os.chdir(folder_path_IN.get())
#     os.chdir("../fullsize_images")

#     for image in correct_label_list:
#         try:
#             shutil.copy("./"+image,folder_path_IN.get()+"/Correct/images/"+image )
#             shutil.copy(folder_path_IN.get()+"/labels/"+image[:-4]+".txt",folder_path_IN.get()+"/Correct/labels/"+image[:-4]+".txt" )
#         except FileNotFoundError:
#             print('Label not found!')
#     for image in incorrect_label_list:
#         try:
#             shutil.copy("./"+image,folder_path_IN.get()+"/Relabel/images/"+image )
#             shutil.copy(folder_path_IN.get()+"/labels/"+image[:-4]+".txt",folder_path_IN.get()+"/Relabel/labels/"+image[:-4]+".txt" )
#         except FileNotFoundError:
#             print('Label not found!')
#     write("Saved")


# # greeting = tk.Label(text="YOLO Image Results",
# #     foreground="black",  # Set the text color to white
# #     background="white",
# #     width=50,
# #     height=5  # Set the background color to black
# # )
# # greeting.grid(row=3,column=0)

# def correct():
#     global bounded_image_name
#     global add_to_correct
#     if bounded_image_name:
#         write("Correct Selected")
#         correct_label_list.append(bounded_image_name)
#     bounded_image_name = next_img()
#     write(f"Correct: {correct_label_list}")
#     write(f"Incorrect: {incorrect_label_list}")
#     add_to_correct = True

    

# def incorrect():
#     global bounded_image_name
#     global add_to_correct
#     if bounded_image_name:
#         write("Incorrect Selected")
#         incorrect_label_list.append(bounded_image_name)
#     bounded_image_name = next_img()
#     write(f"Correct: {correct_label_list}")
#     write(f"Incorrect: {incorrect_label_list}")
#     add_to_correct = False

# def swap_list():
#     global add_to_correct
#     global correct_label_list
#     global incorrect_label_list
#     write("swap")
#     if add_to_correct == True:
#         incorrect_label_list.append(correct_label_list.pop())
#         add_to_correct = False
#     elif add_to_correct == False:
#         correct_label_list.append(incorrect_label_list.pop())
#         add_to_correct = True
#     write(f"Correct: {correct_label_list}")
#     write(f"Incorrect: {incorrect_label_list}")



# buttonCorrect = tk.Button(
#     text="Correct (C)",
#     width=25,
#     height = 4,
#     bg="white",
#     fg="black",
#     command = correct
# )

# buttonIncorrect = tk.Button(
#     text="Incorrect (X)",
#     width=25,
#     height = 4,
#     bg="white",
#     fg="black",
#     command = incorrect
# )
# swapButton = tk.Button(
#     text="Swap (V)s",
#     width=25,
#     height = 4,
#     bg="white",
#     fg="black",
#     command = swap_list
# )

# def handle_keypress(event):
#     """Print the character associated to the key pressed"""
#     if event.char == "x":
#         print("x pressed")
#         incorrect()
#     elif event.char == "c":
#         print("c pressed")
#         correct()
#     elif event.char == "v":
#         print("v pressed")    
#         swap_list()
#     elif event.char == "o":
#         print("o pressed")    
#         browse_button_IN()
#     elif event.char == "s":
#         print("s pressed")    
#         save_output()

# # Bind keypress event to handle_keypress()
# window.bind("<Key>", handle_keypress)

# ## LABELS FOR INPUT OUTPUT
# folder_path_IN = StringVar()
# lbl1 = Label(master=window,textvariable=folder_path_IN)
# prediction_folder = Button(text="Prediction Folder (O)",width=15, command=browse_button_IN)
# panel = tk.Label(window)
# # load_images_button = Button(text="Load Images",width=12, command=load_images)
# button_save = Button(text="Save Output (S)",width=15, command=save_output)


# # Placement
# lbl1.grid(row=0,column=0)
# prediction_folder.grid(row=0,column=1)
# # load_images_button.grid(row=1,column=1)
# button_save.grid(row=2,column=1)
# buttonCorrect.grid(row=3,column=1)
# buttonIncorrect.grid(row=4,column=1)
# swapButton.grid(row=4,column=0)
# panel.grid(row=5,column=0)
# Console.grid(row=1,column=0, rowspan=3)
# # button2 = Button(text="Output",width=10, command=browse_button_OUT)
# # button2.grid(row=1, column=3)

# window.mainloop()