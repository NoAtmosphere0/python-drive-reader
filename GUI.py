import tkinter as tk
from tkinter import ttk

class DriveExplorer:
    def __init__(self, root, data):
        self.root = root
        self.root.title("Python Drive Reader")

        self.treeview = ttk.Treeview(self.root)
        self.treeview.pack(side="left", fill="both", expand=True)

        vsb = ttk.Scrollbar(self.root, orient="vertical", command=self.treeview.yview)
        vsb.pack(side='right', fill='y')

        self.treeview.configure(yscrollcommand=vsb.set)

        self.populate_treeview(data)

    def populate_treeview(self, data, parent=""):
        if isinstance(data, dict):
            for key in data.keys():
                item = self.treeview.insert(parent, 'end', text=key)
                self.populate_treeview(data[key], item)
        elif isinstance(data, list):
            for i, item in enumerate(data):
                self.populate_treeview(item, parent)
        else:
            self.treeview.insert(parent, 'end', text=data)

root = tk.Tk()

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

app = DriveExplorer(root, data)
root.mainloop()
