#from main import SOURCE
from tkinter import filedialog
import tkinter as tk
import platform


def get_source():

   global SOURCE
   global source_name

   SOURCE = filedialog.askdirectory()
   source_name.set(SOURCE)

def get_destination():
   global PROJECT
   global destination_name

   PROJECT = filedialog.askdirectory()
   destination_name.set(PROJECT)
   close_btn['state'] = 'normal'

def close():

   win.destroy()

def load():
   global source_name
   global destination_name
   global win
   global close_btn

   win = tk.Tk()
   if platform.system() == 'Windows' :
      win.geometry("700x500")
   if platform.system() == 'Darwin':
      win.geometry("900x500")
   win.resizable(False, False)

   source_text = tk.StringVar()
   source_btn = tk.Button(win, textvariable=source_text, command=get_source, height=5, width=50)
   source_text.set('Open Source Directory')
   source_btn.grid(column=0, row=0)

   source_name = tk.StringVar()
   l1 = tk.Label(master=win,textvariable=source_name, height=5, width=100)
   l1.grid(column=0, row=1)

   destination_text = tk.StringVar()
   destination_btn = tk.Button(win, textvariable=destination_text, command=get_destination, height=5, width=50)
   destination_text.set('Open Destination Directory')
   destination_btn.grid(column=0, row=2)

   destination_name = tk.StringVar()
   l2 = tk.Label(master=win,textvariable=destination_name, height=5, width=100)
   l2.grid(column=0, row=3)


   close_text = tk.StringVar()
   close_btn = tk.Button(win, textvariable=close_text, command=close, height=3, width=50, state='disabled')
   close_text.set('Begin YOLO Labelling')
   close_btn.grid(column=0, row=4)


   #win.destroy()
   win.mainloop()

   return SOURCE, PROJECT

load()
