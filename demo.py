import struct
import tkinter as tk


# function to read the MBR from a disk
def read_mbr(disk):
    with open(disk, 'rb') as f:
        data = f.read(512)
        return data


# function to parse the MBR and determine the number of partition tables and their styles
def parse_mbr(data):
    mbr_signature = struct.unpack("<H", data[510:512])[0]
    if mbr_signature != 0xAA55:
        raise ValueError("Invalid MBR signature")

    partition_table_offset = 0x1BE
    num_partitions = 0
    partition_styles = []
    for i in range(4):
        partition_type = data[partition_table_offset + 4 + (i * 16)]
        if partition_type == 0x00:
            continue
        num_partitions += 1
        # corresponds to the partition style whether it is FAT32 or NTFS
        if partition_type == 0x0B or partition_type == 0x0C:
            partition_type = "FAT32"
        elif partition_type == 0x07 or partition_type == 0x27 or partition_type == 0x1C or partition_type == 0x1E:
            partition_type = "NTFS"
        partition_styles.append(partition_type)

    return num_partitions, partition_styles


# create the GUI
root = tk.Tk()
root.title("MBR Parser")

# create the labels and text boxes for displaying the results
num_partitions_label = tk.Label(root, text="Number of partition tables:")
num_partitions_label.pack()
num_partitions_text = tk.Text(root, height=1, width=20)
num_partitions_text.pack()
partition_styles_label = tk.Label(root, text="Partition styles:")
partition_styles_label.pack()
partition_styles_text = tk.Text(root, height=4, width=20)
partition_styles_text.pack()


# function to update the GUI with the parsed MBR data
def update_gui():
    disk = "\\\\.\PhysicalDrive1"  # replace with the path to your disk
    data = read_mbr(disk)
    num_partitions, partition_styles = parse_mbr(data)
    num_partitions_text.delete('1.0', tk.END)
    num_partitions_text.insert(tk.END, str(num_partitions))
    partition_styles_text.delete('1.0', tk.END)
    partition_styles_text.insert(tk.END, "\n".join(partition_styles))


# create a button to trigger the MBR parsing
parse_button = tk.Button(root, text="Parse MBR", command=update_gui)
parse_button.pack()

# start the GUI event loop
root.mainloop()