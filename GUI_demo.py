import tkinter as tk
import json
import tkinter.ttk as ttk
import disk_info

class import_data():
    def __init__(self):
        self.data_fat32 = None
        self.data_ntfs = None

        self.data_ntfs = self.read_data_ntfs()
        self.data_fat32 = self.read_data_fat32()

    # Load the data from data.txt into a Python dictionary
    def read_data_ntfs(self):
        with open("data_ntfs.txt", "r") as f:
            data_ntfs = eval(f.read())
        return data_ntfs


    def read_data_fat32(self):
        with open("data_fat32.txt", "r") as j:
            data_fat32 = eval(j.read())
        return data_fat32
    
    def get_data(self):
        print("import data class:")
        print(self.data_ntfs)
        print(self.data_fat32)
        print("___________________________")
        return self.data_ntfs, self.data_fat32


# def import_data_ntfs(self, file_path):
#     with open(file_path, "r") as file:
#         data_ntfs = json.load(file)
#     return data_ntfs


# def import_data_fat32(self, file_path):
#     with open(file_path, "r") as file:
#         data_fat32 = json.load(file)
#     return data_fat32

class process_data():
    def __init__(self):
        import_object = import_data()
        self.data_ntfs, self.data_fat32 = import_object.get_data()

        self.json_data_nfts, self.json_data_fat32 = self.write_to_json()
    def write_to_json(self):
        # Convert the Python dictionary to a JSON-formatted string
        self.json_data_ntfs = json.dumps(self.data_ntfs)
        
        # Write the JSON-formatted string to a new file
        #with open("data_ntfs.json", "w") as f:
            #f.write(self.json_data_ntfs)

        self.json_data_fat32 = json.dumps(self.data_fat32)
        # Write the JSON-formatted string to a new file
        #with open("data_fat32.json", "w") as j:
            #j.write(self.json_data_fat32)

        return self.json_data_ntfs, self.json_data_fat32

    def get_processed_data(self):
        print("process data class:")
        print(self.json_data_ntfs)
        print(self.json_data_fat32)
        print("___________________________")
        return self.data_ntfs, self.data_fat32



class Explorer:
    def __init__(self):
        data = process_data()
        self.data_ntfs, self.data_fat32 = data.get_processed_data()

        #self.data_ntfs = {"$MFT": {"type": "SYSTEM", "size": 262144, "created": "2023-03-08 16:24:36", "modified": "2023-03-08 16:24:36"}, "$MFTMirr": {"type": "SYSTEM", "size": 4096, "created": "2023-03-08 16:24:36", "modified": "2023-03-08 16:24:36"}, "$LogFile": {"type": "SYSTEM", "size": 4341760, "created": "2023-03-08 16:24:36", "modified": "2023-03-08 16:24:36"}, "$Volume": {"type": "SYSTEM", "size": 72, "created": "2023-03-08 16:24:36", "modified": "2023-03-08 16:24:36"}, "$AttrDef": {"type": "SYSTEM", "size": 2560, "created": "2023-03-08 16:24:36", "modified": "2023-03-08 16:24:36"}, "$Bitmap": {"type": "SYSTEM", "size": 131072, "created": "2023-03-08 16:24:36", "modified": "2023-03-08 16:24:36"}, "$Boot": {"type": "SYSTEM", "size": 8192, "created": "2023-03-08 16:24:36", "modified": "2023-03-08 16:24:36"}, "$BadClus": {"type": "SYSTEM", "size": 536870400, "created": "2023-03-08 16:24:36", "modified": "2023-03-08 16:24:36"}, "$Secure": {"type": "SYSTEM", "size": 263324, "created": "2023-03-08 16:24:36", "modified": "2023-03-08 16:24:36"}, "$UpCase": {"type": "SYSTEM", "size": 72, "created": "2023-03-08 16:24:36", "modified": "2023-03-08 16:24:36"}}
        #self.data_fat32 = {"Ref_BT_FAT1.pdf": {"type": "file", "size": 457965, "created": "03/13/2023 16:13:30", "modified": "None"}, "Ref_BT_FAT2.pdf": {"type": "file", "size": 727716, "created": "03/13/2023 16:13:31", "modified": "None"}, "Ref_BT_NTFS.pdf": {"type": "file", "size": 577747, "created": "03/13/2023 16:13:31", "modified": "None"}, "Ref_FAT.pdf": {"type": "file", "size": 178413, "created": "03/13/2023 16:13:32", "modified": "None"}}

        print(type(self.data_ntfs))

        self.root = tk.Tk()
        self.root.title("Disk Explorer")
        self.root.geometry("1200x300")
        # Create a frame for the treeview widget
        frame = ttk.Frame(self.root)  # set the background color to blue
        frame.pack(fill=tk.BOTH, expand=1)
        # modify the frame to add a scrollbar
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        # create a custom style for the frame
        style = ttk.Style(self.root)
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
        style = ttk.Style(self.root)
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

        # Set the command for each column heading to sort the items
        tree.heading(
            "#0",
            text="Name",
            anchor=tk.W,
            command=lambda: self.sort_column(tree, "#0", False),
        )
        tree.heading(
            "#1",
            text="Type",
            anchor=tk.W,
            command=lambda: self.sort_column(tree, "#1", False),
        )
        tree.heading(
            "#2",
            text="Size",
            anchor=tk.W,
            command=lambda: self.sort_column(tree, "#2", False),
        )
        tree.heading(
            "#3",
            text="Date Created",
            anchor=tk.W,
            command=lambda: self.sort_column(tree, "#3", False),
        )
        tree.heading(
            "#4",
            text="Date Modified",
            anchor=tk.W,
            command=lambda: self.sort_column(tree, "#4", False),
        )
        # STATUS BAR

        ## Create a label widget to display the status message
        status_frame = tk.Frame(self.root)
        status_frame.pack(side=tk.TOP, fill=tk.X)
        # Create a new frame for the status bar
        status_bar_frame = tk.Frame(self.root)
        status_bar_frame.pack(side=tk.TOP, fill=tk.X)

        # # Create a label widget to display the status message
        label1 = ttk.Label(status_bar_frame, text=self.get_partition_size(1))
        label2 = ttk.Label(status_bar_frame, text=self.get_partition_size(2))
        label1.pack(side=tk.TOP)
        label2.pack(side=tk.TOP)
        frame.pack(side=tk.TOP, fill=tk.BOTH)

        # BUTTONS

        # Add buttons to the existing button frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(side=tk.BOTTOM, pady=10)

        ntfs_button = tk.Button(
            button_frame,
            text="Load NTFS",
            command=lambda: self.add_items("", self.data_ntfs),
        )
        ntfs_button.pack(side=tk.LEFT, padx=10)

        fat32_button = tk.Button(
            button_frame,
            text="Load FAT32",
            command=lambda: self.add_items("", self.data_fat32),
        )
        fat32_button.pack(side=tk.RIGHT, padx=10)

        # Add the "Quit" button to the buttons frame
        quit_button = tk.Button(button_frame, text="Quit", command=self.root.quit)
        quit_button.pack(side=tk.RIGHT, padx=10)

        clear_button = tk.Button(
            button_frame, text="Clear", command=self.clear_treeview
        )
        clear_button.pack(side=tk.RIGHT, padx=10)

        # Add the "Refresh" button to the buttons frame
        refresh_button = tk.Button(
            button_frame, text="Refresh", command=self.update_status_bar
        )
        refresh_button.pack(side=tk.RIGHT, padx=10)
        self.root.mainloop()
        pass

    def add_items(self, parent, items):
        for key, value in items.items():
            tags = ()
            if value.get("type") == "folder":
                tags = ("folder",)
            if value.get("type") == "file":
                tags = ("file",)
            print(value)
            node = self.tree.insert(
                parent,
                "end",
                text=key,
                values=[
                    value.get('type', ""),
                    value.get('size', ""),
                    value.get('created', ""),
                    value.get('modified', ""),
                ],
                tags=tags,
            )
            if isinstance(value, dict):
                self.add_items(node, value.get("contents", {}))

    # Sort the treeview items by clicking on the column headings (optional)
    def sort_column(self, tree, col, reverse):
        # Get the list of items in the tree
        items = [(tree.set(child, col), child) for child in tree.get_children("")]
        # Sort the items based on the column value
        items.sort(reverse=reverse)
        for index, (val, child) in enumerate(items):
            # Re-order the items in the tree
            tree.move(child, "", index)
        # Reverse the sort direction for the next click
        tree.heading(col, command=lambda: self.sort_column(tree, col, not reverse))

    def clear_treeview(self):
        for child in self.tree.get_children():
            self.tree.delete(child)

    def get_partition_size(self, choice):
        try:
            pt = disk_info.MBR(r"\\.\PhysicalDrive1")
            partitions = pt.get_partitions()
            ntfs_size = f"NTFS partition size: {partitions['NTFS'][1] / 1024 / 1024} MB"
            fat32_size = (
                f"FAT32 partition size: {partitions['FAT32'][1] / 1024 / 1024}  MB"
            )
            if choice == 1:
                return ntfs_size
            elif choice == 2:
                return fat32_size
        except disk_info.NoDiskFound:
            return "No USB found"

    def update_status_bar(self):
        self.label1.config(text=self.get_partition_size(1))
        self.label2.config(text=self.get_partition_size(2))
        self.root.after(1000, self.update_status_bar)
