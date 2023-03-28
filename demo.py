import os
import tkinter as tk
from tkinter import ttk


class FileExplorer:
    def __init__(self, root):
        self.root = root
        self.root.title("File Explorer")

        # Create the Treeview widget
        self.treeview = ttk.Treeview(root)

        # Define the columns
        self.treeview["columns"] = ("size", "type", "modified")

        # Format the columns
        self.treeview.column("#0", width=250, stretch=tk.YES)
        self.treeview.column("size", width=100, stretch=tk.NO)
        self.treeview.column("type", width=100, stretch=tk.NO)
        self.treeview.column("modified", width=150, stretch=tk.NO)

        # Create the headings
        self.treeview.heading("#0", text="File Name", anchor=tk.W)
        self.treeview.heading("size", text="File Size", anchor=tk.W)
        self.treeview.heading("type", text="File Type", anchor=tk.W)
        self.treeview.heading("modified", text="Modified Date", anchor=tk.W)

        # Add the root node
        self.root_node = self.treeview.insert("", "end", text="C:/", open=True)

        # Populate the Treeview
        self.populate_tree(self.root_node)

        # Add the Treeview to the GUI
        self.treeview.pack(expand=tk.YES, fill=tk.BOTH)

    def populate_tree(self, parent):
        # Get the directory contents
        path = self.treeview.set(parent, "#0")
        for item in os.listdir(path):
            # Get the item path
            item_path = os.path.join(path, item)

            # Determine if the item is a directory
            isdir = os.path.isdir(item_path)

            # Insert the item into the Treeview
            if isdir:
                item_id = self.treeview.insert(parent, "end", text=item, open=False)
                self.populate_tree(item_id)
            else:
                size = os.path.getsize(item_path)
                typ = os.path.splitext(item)[1]
                modified = os.path.getmtime(item_path)
                self.treeview.insert(
                    parent, "end", text=item, values=(size, typ, modified)
                )


# Create the GUI
root = tk.Tk()
file_explorer = FileExplorer(root)
root.mainloop()
