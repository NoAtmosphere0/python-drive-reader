import os
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.title("Python Drive reader")

# Create a frame to hold the listbox and scrollbar
frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=1)

# Create a listbox to display the files and folders
listbox = tk.Listbox(frame)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

# Create a scrollbar for the listbox
scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Link the scrollbar and the listbox
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

# Add the files and folders to the listbox
def fill_listbox(path):
    listbox.delete(0, tk.END)
    for file in os.listdir(path):
        listbox.insert(tk.END, file)

# Create a button to choose the directory
def choose_dir():
    path = filedialog.askdirectory()
    fill_listbox(path)

button = tk.Button(root, text="Choose directory", command=choose_dir)
button.pack()

# Fill the listbox with the default directory
fill_listbox(os.getcwd())

root.mainloop()
