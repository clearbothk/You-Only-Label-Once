from tkinter import filedialog
import tkinter as tk

def load_folder(title):

   win = tk.Tk()
   win.title(title)
   win.geometry("700x700")
   filename = filedialog.askdirectory()
   win.destroy()
   win.mainloop()

   return filename


#path = tk.Button(window, text='Select Source Folder', command=load_folder)

#folder_path_IN = StringVar()
#lbl1 = Label(master=window,textvariable=folder_path_IN)
#prediction_folder = Button(text="Prediction Folder (O)",width=15, command=browse_button_IN)

# path.pack()
# window.mainloop()