import tkinter as tk
from tkinter import ttk

data = {
    "filename": {
        "type": "file",
        "size": 1234,
        "created": "2022-01-01 12:34:56",
        "modified": "2022-02-02 23:45:01"
    },
    "foldername": {
        "type": "folder",
        "created": "2022-01-01 12:34:56",
        "modified": "2022-02-02 23:45:01",
        "contents": {
            "filename": {
                "type": "file",
                "size": 5678,
                "created": "2022-01-02 12:34:56",
                "modified": "2022-02-03 23:45:01"
            },
            "subfoldername": {
                "type": "folder",
                "created": "2022-01-03 12:34:56",
                "modified": "2022-02-04 23:45:01",
                "contents": {
                    "filename": {
                        "type": "file",
                        "size": 91011,
                        "created": "2022-01-04 12:34:56",
                        "modified": "2022-02-05 23:45:01"
                    }
                }
            }
        }
    }
}

def add_items(parent, items):
    for key, value in items.items():
        node = tree.insert(parent, 'end', text=key, values=[value.get('type', ''), value.get('size', ''), value.get('created', ''), value.get('modified', '')])
        if isinstance(value, dict):
            add_items(node, value.get('contents', {}))

# Create the GUI window
root = tk.Tk()
root.title("Disk Explorer")
root.geometry("600x300")

# Create a frame for the treeview widget
frame = ttk.Frame(root)
frame.pack(fill=tk.BOTH, expand=1)

# Create a treeview widget
tree = ttk.Treeview(frame, columns=('Type', 'Size', 'Created', 'Modified'), selectmode='browse')
tree.pack(fill=tk.BOTH, expand=1)

# Create the treeview columns
tree.heading('#0', text='Name', anchor=tk.W)
tree.heading('#1', text='Type', anchor=tk.W)
tree.heading('#2', text='Size', anchor=tk.W)
tree.heading('#3', text='Created', anchor=tk.W)
tree.heading('#4', text='Modified', anchor=tk.W)

# Create the treeview scrollbar
scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
tree.configure(yscrollcommand=scrollbar.set)







# Add the data to the tree
add_items('', data)

root.mainloop()
