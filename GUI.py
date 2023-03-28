import tkinter as tk
from tkinter import ttk
import NTFS
import os
import FAT32
import json
import platform
import subprocess
import tkinter as tk
import win32api


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


# Create the GUI window
root = tk.Tk()
root.title("Disk Explorer")
root.geometry("1000x300")

# Create a frame for the treeview widget
frame = ttk.Frame(root)
frame.pack(fill=tk.BOTH, expand=1)
# modify the frame to add a scrollbar
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)


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
    background="#00FFFF",
    foreground="darkblue",
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


def detect_usb_formats():
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split("\000")[:-1]
    usb_drives = [
        drive for drive in drives if "removable" in win32api.GetVolumeInformation(drive)
    ]
    partitions = {}
    for usb_drive in usb_drives:
        cmd = [
            "wmic",
            "partition",
            "where",
            f"DriveLetter='{usb_drive[:-1]}'",
            "get",
            "Name,FileSystem",
            "/format:list",
        ]
        output = subprocess.check_output(cmd, universal_newlines=True)

        # parse the output to extract the partition names and file systems
        for line in output.splitlines():
            if line.startswith("Name="):
                partition_name = line.split("=")[1]
            elif line.startswith("FileSystem="):
                file_system = line.split("=")[1]
                partitions[partition_name] = file_system

    return partitions


# Create a status bar
def show_usb_formats():
    partitions = detect_usb_formats()
    text_widget = tk.Text(root, height=50, width=100)
    for partition_name, file_system in partitions.items():
        text_widget.insert(tk.END, f"{partition_name}: {file_system}\n")

    status_bar = tk.Label(
        root,
        text=f"USB Status: {', '.join(partitions.values())}",
        bd=1,
        relief=tk.SUNKEN,
        anchor=tk.W,
    )

    status_bar.pack(side=tk.TOP, fill=tk.X, ipady=10)


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


if __name__ == "__main__":
    show_usb_formats()
    root.mainloop()
