#from main import SOURCE
from tkinter import filedialog
import tkinter as tk
import platform

def load(window):

   def get_source():
      global SOURCE
      global source_name
      win.attributes('-topmost', False)
      SOURCE = filedialog.askdirectory()
      source_name.set(SOURCE)
      win.lift()
      win.update()

   def get_destination():
      global PROJECT
      global destination_name
      win.attributes('-topmost', False)
      PROJECT = filedialog.askdirectory()
      destination_name.set(PROJECT)
      win.lift()
      win.update()

   def get_yolo():
      global YOLO
      global yolo_name
      win.attributes('-topmost', False)
      YOLO = filedialog.askdirectory()
      yolo_name.set(YOLO)
      win.lift()
      win.update()

   def close():
      global close_name
      counter = 0

      try:
         if SOURCE:
            counter += 1
      except NameError:
         close_name.set('Source directory not found')
         return 

      try:
         if PROJECT:
            counter += 1
      except NameError:
         close_name.set('Destination directory not found')
         return

      try:
         if YOLO:
            counter += 1
      except NameError:
         close_name.set('YOLO directory not found')
         return

      if SOURCE == PROJECT:
         close_name.set('Source and destination directories cannot be the same!')
      else:
         if counter == 3:
            # win.destroy()
            win.quit()
            
            win.update()



   global source_name
   global destination_name
   global yolo_name
   global close_name
   global win
   global close_btn

   win = tk.Toplevel(window)
   win.title('Load Directories')
   if platform.system() == 'Windows' :
      win.geometry("700x650")
   if platform.system() == 'Darwin':
      win.geometry("900x750")
   win.resizable(False, False)

   source_text = tk.StringVar()
   source_btn = tk.Button(win, textvariable=source_text, command=get_source, height=5, width=50)
   source_text.set('Open Source Directory')
   source_btn.grid(column=0, row=0)

   source_name = tk.StringVar()
   source_name.set('Select source folder where input images are saved')
   l1 = tk.Label(master=win,textvariable=source_name, height=5, width=100)
   l1.grid(column=0, row=1)

   destination_text = tk.StringVar()
   destination_btn = tk.Button(win, textvariable=destination_text, command=get_destination, height=5, width=50)
   destination_text.set('Open Destination Directory')
   destination_btn.grid(column=0, row=2)

   destination_name = tk.StringVar()
   destination_name.set('Select root project folder')
   l2 = tk.Label(master=win,textvariable=destination_name, height=5, width=100)
   l2.grid(column=0, row=3)

   yolo_text = tk.StringVar()
   yolo_btn = tk.Button(win, textvariable=yolo_text, command=get_yolo, height=5, width=50)
   yolo_text.set('Open YOLO Directory')
   yolo_btn.grid(column=0, row=4)

   yolo_name = tk.StringVar()
   yolo_name.set('Select where YOLOv5 folder will be or is installed')
   l3 = tk.Label(master=win,textvariable=yolo_name, height=5, width=100)
   l3.grid(column=0, row=5)

   close_text = tk.StringVar()
   close_btn = tk.Button(win, textvariable=close_text, command=close, height=3, width=50)
   close_text.set('Begin YOLO Labelling')
   close_btn.grid(column=0, row=6)

   close_name = tk.StringVar()
   l4 = tk.Label(master=win,textvariable=close_name, height=5, width=100)
   l4.grid(column=0, row=7)

   print('load finished')
   #win.destroy()
   #win.lift()
   #win.call('wm', 'attributes', '.', '-topmost', True)
   win.attributes('-topmost', True)
   
   win.mainloop()


   win.destroy()
   return SOURCE, PROJECT, YOLO

