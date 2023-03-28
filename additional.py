# # create class for menu items to be added to the right click menu (optional)
# class Menu:
#     def __init__(self, text, command):
#         self.text = text
#         self.command = command


# # Create Menu for right click on treeview item (optional)
# def on_right_click(event):
#     # Select the item under the cursor
#     item = tree.identify("item", event.x, event.y)
#     tree.selection_set(item)

#     # Create a command create a new folder (optional)
#     def new_folder():
#         tree.insert(
#             item,
#             "end",
#             text="New Folder",
#             values=["folder", "", "", ""],
#             tags=("folder",),
#         )

#     # convert the treeview item to a dictionary
#     def treeview_to_dict(tree):
#         d = {tree.item(item)["text"]: {} for item in tree.get_children()}
#         for key, value in d.items():
#             # get the children of the item
#             children = tree.get_children(item)
#             if children:
#                 d[key] = treeview_to_dict(tree)
#         return d

#     # Save new folder to data.json
#     def save_folder():
#         with open("data.json", "w") as f:
#             json.dump(treeview_to_dict(tree), f, indent=4)

#     # auto save new folder to data.json every 5 seconds (optional)
#     root.after(5000, save_folder)

#     def treeview_from_dict(tree, d):
#         for key, value in d.items():
#             if isinstance(value, dict):
#                 item = tree.insert("", "end", text=key, tags=("folder",))
#                 treeview_from_dict(tree, value)
#             else:
#                 tree.insert("", "end", text=key, values=value, tags=("file",))

#     # auto insert new_folder from data.json to treeview (optional)
#     def load_folder():
#         with open("data.json", "r") as f:
#             data = json.load(f)
#             treeview_from_dict(tree, data)

#     # Create a command to delete the selected item (optional)
#     def delete_item():
#         tree.delete(item)

#     # Create a command to rename the selected item (optional)

#     # Create a command to create a new file (optional)
#     def new_file():
#         tree.insert(
#             item,
#             "end",
#             text="New File",
#             values=["file", "", "", ""],
#             tags=("file",),
#         )

#     def rename_item():
#         tree.edit(item)

#     # create a command to show the properties of the selected item (optional)
#     def show_properties():
#         print("Properties")

#     # Display the menu
#     menu = tk.Menu(root, tearoff=0)
#     menu.add_command(label="New Folder", command=new_folder)
#     menu.add_command(label="New File", command=new_file)

#     menu.add_command(label="Delete", command=delete_item)
#     menu.add_command(label="Properties", command=show_properties)

#     menu.post(event.x_root, event.y_root)

#     # Save the input data to data_demo.py (optional)


# # Bind the right-click event to the treeview widget
# tree.bind("<Button-3>", on_right_click)


# def get_items(tree, parent):
#     # Get the data from the treeview
#     items = []
#     for item in parent:
#         # Get the item's text and values
#         text = tree.item(item, "text")
#         values = tree.item(item, "values")
#         # Get the item's children
#         children = tree.get_children(item)
#         # Create a dictionary for the item's data
#         item_data = {
#             "text": text,
#             "values": values,
#             "contents": get_items(tree, children),
#         }
#         # Add the item's data to the list
#         items.append(item_data)
#     return items


# # convert the treeview to a dictionary and save it to data_demo.py (optional)
# def save_data():
#     # Get the data from the treeview
#     data = get_items(tree, tree.get_children())
#     # Save the data to the filen
#     with open("data.txt", "w") as f:
#         f.write("data = " + str(data))

# import tkinter as tk
# import subprocess
# import platform
# import os
# import json

# # Create a Tkinter window
# window = tk.Tk()

# # Set the window title
# window.title("Partition Viewer")

# # Set the window size
# window.geometry("500x500")


# # Function to read data from JSON file
# def read_json_data(partition):
#     with open(f"data_{partition}.json") as f:
#         data = json.load(f)
#     return data


# # Function to display partition information
# def display_partition_info(partition):
#     if platform.system() == "Windows":
#         cmd = f"wmic logicaldisk where caption='{partition.upper()}:\\' get size,freespace /format:list"
#         output = subprocess.check_output(cmd, shell=True)
#         output = output.decode("utf-8").strip().split("\r\r\n")
#         disk_size = output[1].split("=")[1]
#         free_space = output[2].split("=")[1]
#         info_label.config(text=f"Disk Size: {disk_size}\nFree Space: {free_space}")
#     else:
#         info_label.config(text="Partition info not available on this platform.")


# # Function to display partition data
# def display_partition_data(partition):
#     data = read_json_data(partition)
#     data_label.config(text=json.dumps(data, indent=4))


# # Create a menu bar
# menu_bar = tk.Menu(window)

# # Create a Partition menu
# partition_menu = tk.Menu(menu_bar, tearoff=0)

# # Add the NTFS partition to the menu
# partition_menu.add_command(
#     label="NTFS",
#     command=lambda: [display_partition_data("ntfs"), display_partition_info("ntfs")],
# )

# # Add the FAT32 partition to the menu
# partition_menu.add_command(
#     label="FAT32",
#     command=lambda: [display_partition_data("fat32"), display_partition_info("fat32")],
# )

# # Add the Partition menu to the menu bar
# menu_bar.add_cascade(label="Partition", menu=partition_menu)

# # Add the menu bar to the window
# window.config(menu=menu_bar)

# # Create a label to display partition information
# info_label = tk.Label(
#     window, text="Select a partition from the Partition menu to view its information."
# )
# info_label.pack()

# # Create a label to display partition data
# data_label = tk.Label(window, text="")
# data_label.pack()

# # Run the Tkinter event loop
# window.mainloop()
