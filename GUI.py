import subprocess
import tkinter as tk
import psutil
import sys
import json
import tkinter.ttk as ttk
import os


def import_data_ntfs(file_path):
    with open(file_path, "r") as file:
        data_ntfs = json.load(file)
    return data_ntfs


data_ntfs = import_data_ntfs("data_ntfs.txt")


# Load the data from data.txt into a Python dictionary
def read_data_ntfs():
    with open("data_ntfs.txt", "r") as f:
        data_ntfs = eval(f.read())
    return data_ntfs


data_ntfs = read_data_ntfs()
# Convert the Python dictionary to a JSON-formatted string
json_data_ntfs = json.dumps(data_ntfs)
# Write the JSON-formatted string to a new file
with open("data_ntfs.json", "w") as f:
    f.write(json_data_ntfs)


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


def clear_treeview():
    for child in tree.get_children():
        tree.delete(child)


usb_partitions = []

# Get a list of all the partitions on the system
partitions = psutil.disk_partitions()

# Filter the partitions to only include those that are on a USB device
for partition in partitions:
    if "removable" in partition.opts:
        usb_partitions.append(partition.mountpoint)

# Create a status bar with the list of USB partitions
status_bar = "USB partitions: "
for partition in usb_partitions:
    status_bar += partition + " "

# Display the status bar
os.system('echo "' + status_bar + '"')


def update_statusbar():
    global statusbar
    global data_ntfs
    global data_fat32

    # Calculate the total size and used size of the NTFS partition
    total_ntfs = sum(value.get("size", 0) for value in data_ntfs.values())
    used_ntfs = sum(
        value.get("size", 0) for value in data_ntfs.values() if value.get("used", False)
    )
    ntfs_status = f"NTFS Partition: {used_ntfs/total_ntfs*100:.2f}% Used"

    # # Calculate the total size and used size of the FAT32 partition
    # total_fat32 = sum(value.get("size", 0) for value in data_fat32.values())
    # used_fat32 = sum(
    #     value.get("size", 0)
    #     for value in data_fat32.values()
    #     if value.get("used", False)
    # )
    # fat32_status = f"FAT32 Partition: {used_fat32/total_fat32*100:.2f}% Used"

    # Update the statusbar with the partition statuses
    statusbar["text"] = f"{ntfs_status} "


# Create the Clear button


# Place the button on the bottom right side of the frame


# Create a frame for the buttons
button_frame = ttk.Frame(root)
button_frame.pack(side=tk.BOTTOM, pady=10)

ntfs_button = tk.Button(
    button_frame, text="Load NTFS", command=lambda: add_items("", data_ntfs)
)
ntfs_button.pack(side=tk.LEFT, padx=10)

fat32_button = tk.Button(button_frame, text="Load FAT32")
fat32_button.pack(side=tk.RIGHT, padx=10)

# Add the "Refresh" button to the buttons frame
refresh_button = ttk.Button(button_frame, text="Refresh", command=update_statusbar)
refresh_button.pack(side=tk.LEFT, padx=5, pady=5)

# Add the "Quit" button to the buttons frame
quit_button = ttk.Button(button_frame, text="Quit", command=root.quit)
quit_button.pack(side=tk.RIGHT, padx=5, pady=5)

clear_button = ttk.Button(button_frame, text="Clear", command=clear_treeview)
clear_button.pack(side=tk.RIGHT, padx=5, pady=5)

# Create the status bar, modify the status bar to include the USB partitions and the NTFS and FAT32 partition statuses (optional)
status_bar = ttk.Label(root, text=status_bar, relief=tk.SUNKEN, anchor=tk.W)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)


# Add the NTFS status label to the status bar
ntfs_status = tk.StringVar()
ntfs_status.set("USB Format")
ntfs_label = ttk.Label(status_bar, textvariable=ntfs_status)
ntfs_label.pack(side=tk.LEFT)


# Add the FAT32 status label to the status bar
fat32_status = tk.StringVar()
fat32_status.set("FAT32: -")
fat32_label = ttk.Label(status_bar, textvariable=fat32_status)
fat32_label.pack(side=tk.RIGHT)


#     # Update the status bar every 1 second
#     root.after(1000, update_statusbar)
#     # Create the status bar


# create_statusbar(root)
# Create the buttons frame
buttons_frame = ttk.Frame(root)
buttons_frame.pack(side=tk.BOTTOM)


root.mainloop()
