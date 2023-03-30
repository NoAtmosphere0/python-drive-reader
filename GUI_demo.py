import tkinter as tk
import json
import tkinter.ttk as ttk
import disk_info


def import_data_ntfs(file_path):
    with open(file_path, "r") as file:
        data_ntfs = json.load(file)
    return data_ntfs


def import_data_fat32(file_path):
    with open(file_path, "r") as file:
        data_fat32 = json.load(file)
    return data_fat32


data_ntfs = import_data_ntfs("data_ntfs.txt")
dat_fat32 = import_data_fat32("data_fat32.txt")


# Load the data from data.txt into a Python dictionary
def read_data_ntfs():
    with open("data_ntfs.txt", "r") as f:
        data_ntfs = eval(f.read())
    return data_ntfs


def read_data_fat32():
    with open("data_fat32.txt", "r") as j:
        data_fat32 = eval(j.read())
    return data_fat32


data_ntfs = read_data_ntfs()
data_fat32 = read_data_fat32()

# Convert the Python dictionary to a JSON-formatted string
json_data_ntfs = json.dumps(data_ntfs)
# Write the JSON-formatted string to a new file
with open("data_ntfs.json", "w") as f:
    f.write(json_data_ntfs)

json_data_fat32 = json.dumps(data_fat32)
# Write the JSON-formatted string to a new file
with open("data_fat32.json", "w") as j:
    j.write(json_data_fat32)


class Explorer:
    def __init__(self):
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
            command=lambda: self.add_items("", data_ntfs),
        )
        ntfs_button.pack(side=tk.LEFT, padx=10)

        fat32_button = tk.Button(
            button_frame,
            text="Load FAT32",
            command=lambda: self.add_items("", data_fat32),
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
            node = self.tree.insert(
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
