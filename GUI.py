import tkinter as tk
from tkinter import ttk
import NTFS
import os
import FAT32
import json
import platform
import subprocess
import tkinter as tk
import psutil
import sys

sys.setrecursionlimit(10000)


def import_data(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    return data


data = import_data("data.txt")


# Load the data from data.txt into a Python dictionary
def read_data():
    with open("data.txt", "r") as f:
        data = eval(f.read())
    return data


data = read_data()

# Convert the Python dictionary to a JSON-formatted string
json_data = json.dumps(data)

# Write the JSON-formatted string to a new file
with open("data.json", "w") as f:
    f.write(json_data)


def add_items(parent, items):
    for key, value in items.items():
        tags = ()
        if value.get("type") == "folder":
            tags = ("folder",)
        if value.get("type") == "file":
            tags = ("file",)
        node = tree.insert(
            parent,
            "end",
            text=key,
            values=[
                value.get("type", ""),
                value.get("size", ""),
                value.get("created", ""),
                value.get("modified", ""),
            ],
            tags=tags,
        )
        if isinstance(value, dict):
            add_items(node, value.get("contents", {}))

    # Configure the font for the treeview item's text
    tree.tag_configure(
        "folder",
        font=(
            "Segoe UI",
            12,
        ),
    )
    tree.tag_configure(
        "file",
        font=(
            "Segoe UI",
            12,
        ),
    )


root = tk.Tk()
root.title("Disk Explorer")
root.geometry("1200x300")

# Create a frame for the treeview widget
frame = ttk.Frame(root)  # set the background color to blue
frame.pack(fill=tk.BOTH, expand=1)

# modify the frame to add a scrollbar
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

# create a custom style for the frame
style = ttk.Style(root)
style.configure(
    "Frame",
    background="#00FFFF",
    foreground="darkblue",
)

# Create a treeview widget
tree = ttk.Treeview(
    frame,
    columns=("Type", "Size", "Date Created", "Date Modified"),
    selectmode="browse",
)
tree.pack(fill=tk.BOTH, expand=1)
# Create a custom style for the heading
style = ttk.Style(root)

style.configure(
    "Treeview.Heading",
    background="#FF80AA",
    foreground="black",
    font=(
        "Segoe UI",
        14,
    ),
)


# Create the treeview columns with the custom style
tree.heading("#0", text="Name", anchor=tk.W)
tree.heading("#1", text="Type", anchor=tk.W)
tree.heading("#2", text="Size", anchor=tk.W)
tree.heading("#3", text="Date Created", anchor=tk.W)
tree.heading("#4", text="Date Modified", anchor=tk.W)

# Set the column widths
tree.column("#0", minwidth=200, width=400)
tree.column("#1", minwidth=100, width=150)
tree.column("#2", minwidth=100, width=150)
tree.column("#3", minwidth=150, width=200)
tree.column("#4", minwidth=150, width=200)


# Sort the treeview items by clicking on the column headings (optional)
def sort_column(tree, col, reverse):
    # Get the list of items in the tree
    items = [(tree.set(child, col), child) for child in tree.get_children("")]

    # Sort the items based on the column value
    items.sort(reverse=reverse)

    for index, (val, child) in enumerate(items):
        # Re-order the items in the tree
        tree.move(child, "", index)

    # Reverse the sort direction for the next click
    tree.heading(col, command=lambda: sort_column(tree, col, not reverse))


# Set the command for each column heading to sort the items
tree.heading(
    "#0", text="Name", anchor=tk.W, command=lambda: sort_column(tree, "#0", False)
)
tree.heading(
    "#1", text="Type", anchor=tk.W, command=lambda: sort_column(tree, "#1", False)
)
tree.heading(
    "#2", text="Size", anchor=tk.W, command=lambda: sort_column(tree, "#2", False)
)
tree.heading(
    "#3",
    text="Date Created",
    anchor=tk.W,
    command=lambda: sort_column(tree, "#3", False),
)
tree.heading(
    "#4",
    text="Date Modified",
    anchor=tk.W,
    command=lambda: sort_column(tree, "#4", False),
)


def create_statusbar(root):
    # Create the status bar
    statusbar = tk.Label(
        root,
        text="USB Format: Unknown",
        bd=1,
        relief=tk.SUNKEN,
        anchor="center",
        background="#7FFFD4",
        foreground="black",
        font=("Segoe UI", 12),
    )
    statusbar.pack(side=tk.BOTTOM, fill=tk.X, ipady=10)

    # Update the status bar with the USB format
    def update_statusbar():
        partitions = psutil.disk_partitions()
        for partition in partitions:
            if "removable" in partition.opts:
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    format = partition.fstype
                    statusbar.config(
                        text=f"USB Format: {format} ({usage.free / 1024 / 1024:.2f} MB free)"
                    )
                    return
                except:
                    pass
        statusbar.config(text="USB Format: Unknown")

    # Update the status bar every 1 second
    root.after(1000, update_statusbar)

    # Create the status bar


create_statusbar(root)

# Create a frame for the treeview widget
frame = ttk.Frame(root)


# create class for menu items to be added to the right click menu (optional)
class Menu:
    def __init__(self, text, command):
        self.text = text
        self.command = command


# Create Menu for right click on treeview item (optional)
def on_right_click(event):
    # Select the item under the cursor
    item = tree.identify("item", event.x, event.y)
    tree.selection_set(item)

    # Create a command create a new folder (optional)
    def new_folder():
        tree.insert(
            item,
            "end",
            text="New Folder",
            values=["folder", "", "", ""],
            tags=("folder",),
        )

    # convert the treeview item to a dictionary
    def treeview_to_dict(tree):
        d = {tree.item(item)["text"]: {} for item in tree.get_children()}
        for key, value in d.items():
            # get the children of the item
            children = tree.get_children(item)
            if children:
                d[key] = treeview_to_dict(tree)
        return d

    # Save new folder to data.json
    def save_folder():
        with open("data.json", "w") as f:
            json.dump(treeview_to_dict(tree), f, indent=4)

    # auto save new folder to data.json every 5 seconds (optional)
    root.after(5000, save_folder)

    def treeview_from_dict(tree, d):
        for key, value in d.items():
            if isinstance(value, dict):
                item = tree.insert("", "end", text=key, tags=("folder",))
                treeview_from_dict(tree, value)
            else:
                tree.insert("", "end", text=key, values=value, tags=("file",))

    # auto insert new_folder from data.json to treeview (optional)
    def load_folder():
        with open("data.json", "r") as f:
            data = json.load(f)
            treeview_from_dict(tree, data)

    # Create a command to delete the selected item (optional)
    def delete_item():
        tree.delete(item)

    # Create a command to rename the selected item (optional)

    # Create a command to create a new file (optional)
    def new_file():
        tree.insert(
            item,
            "end",
            text="New File",
            values=["file", "", "", ""],
            tags=("file",),
        )

    def rename_item():
        tree.edit(item)

    # create a command to show the properties of the selected item (optional)
    def show_properties():
        print("Properties")

    # Display the menu
    menu = tk.Menu(root, tearoff=0)
    menu.add_command(label="New Folder", command=new_folder)
    menu.add_command(label="New File", command=new_file)

    menu.add_command(label="Delete", command=delete_item)
    menu.add_command(label="Properties", command=show_properties)

    menu.post(event.x_root, event.y_root)

    # Save the input data to data_demo.py (optional)


# Bind the right-click event to the treeview widget
tree.bind("<Button-3>", on_right_click)


def get_items(tree, parent):
    # Get the data from the treeview
    items = []
    for item in parent:
        # Get the item's text and values
        text = tree.item(item, "text")
        values = tree.item(item, "values")
        # Get the item's children
        children = tree.get_children(item)
        # Create a dictionary for the item's data
        item_data = {
            "text": text,
            "values": values,
            "contents": get_items(tree, children),
        }
        # Add the item's data to the list
        items.append(item_data)
    return items


# convert the treeview to a dictionary and save it to data_demo.py (optional)
def save_data():
    # Get the data from the treeview
    data = get_items(tree, tree.get_children())
    # Save the data to the filen
    with open("data.txt", "w") as f:
        f.write("data = " + str(data))


# Add the data to the tree
add_items("", data)


root.mainloop()
