import os
import time
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from disk_info import MBR, partition_table
from FAT32 import FAT32
from NTFS import NTFS
class FileExplorer:
    def __init__(self, master):
        self.master = master
        self.master.title("PYTHON DRIVE READER")
        
        # Create the directory path label
        self.dir_label = tk.Label(self.master, text="Directory Path:")
        self.dir_label.grid(row=0, column=0)
        
        # Create the directory path entry widget
        self.dir_entry = tk.Entry(self.master, width=50)
        self.dir_entry.grid(row=0, column=1)
        
        # Create the browse button
        self.browse_button = tk.Button(self.master, text="Browse", command=self.browse_directory)
        self.browse_button.grid(row=0, column=2)
        
        # Create the file listbox
        self.file_listbox = tk.Listbox(self.master, width=70)
        self.file_listbox.grid(row=1, column=0, columnspan=3)
        
        # Set up the file listbox scrollbar
        self.file_scrollbar = tk.Scrollbar(self.master, orient=tk.VERTICAL)
        self.file_scrollbar.grid(row=1, column=3, sticky="NS")
        self.file_listbox.config(yscrollcommand=self.file_scrollbar.set)
        self.file_scrollbar.config(command=self.file_listbox.yview)
        
        # Populate the file listbox with the files in the initial directory
        self.current_directory = os.getcwd()
        self.populate_file_listbox(self.current_directory)
        
    def browse_directory(self):
        # Open a file dialog to allow the user to select a directory
        selected_directory = filedialog.askdirectory()
        
        if selected_directory:
            # Update the directory path entry widget and current directory variable
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, selected_directory)
            self.current_directory = selected_directory
            
            # Populate the file listbox with the files in the selected directory
            self.populate_file_listbox(self.current_directory)
            
    def populate_file_listbox(self, directory):
        # Clear the file listbox
        self.file_listbox.delete(0, tk.END)
        
        # Get a list of the files in the directory
        files = os.listdir(directory)
        
        # Add each file to the file listbox
        for file in files:
            self.file_listbox.insert(tk.END, file)
    def get_file_info(path):
    
        info = {}
        info["name"] = os.path.basename(path)
        info["path"] = path
        info["size"] = os.path.getsize(path)
        info["modified"] = os.path.getmtme(path)
        return info
    
    def get_click_path(self):
        # Get the index of the selected file
        selected_index = self.file_listbox.curselection()[0]
        
        # Get the name of the selected file
        selected_file = self.file_listbox.get(selected_index)
        
        # Get the full path of the selected file
        selected_path = os.path.join(self.current_directory, selected_file)
        
        return selected_path
    def double_clicked (self, event):
        path = self.get_click_path()
        if os.path.isdir(path):
            self.populate_file_listbox(path)
        else:
            self.open_file(path)
        

        
# Create the application window and start the main event loop
root = tk.Tk()
app = FileExplorer(root)
root.mainloop()
