""""This file contains the MBR and partition table class
    which is used to read and extract information the MBR and partition table"""

# TODO: Create function(s) to parse the MBR 
# TODO: and determine the number of partition tables and their styles
""""Which includes: total number of partitions, their types, and their sizes and 
    locations on the disk."""

class MBR:
    def __init__(self, drive) -> None: # Does not need to take any parameters
        self.data = None
        self.status = None
        self.partition_type = None
        self.starting_sector = None
        self.total_sectors = None
        with open(drive, 'rb') as mbr:
            self.data = mbr.read(446)
            self.status = hex(int.from_bytes(self.data[0:1], byteorder='little'))
            self.partition_type = hex(int.from_bytes(self.data[4:5], byteorder='little'))
            self.starting_sector = int.from_bytes(self.data[8:12], byteorder='little')
            self.total_sectors = int.from_bytes(self.data[12:16], byteorder='little')

    def printMBR(self):
        print("MBR data: ")
        print("Status: ", self.status)
        print("Partition type: ", self.partition_type)
        print("Starting sector: ", self.starting_sector)
        print("Total sectors: ", self.total_sectors)
        print("----------------------------------")
class partition_table:
    def __init__(self) -> None:
        self.offset = 0x1BE
        self.size = 0x10
    def read(self, drive):
        with open(drive, 'rb') as f:
            f.seek(self.offset)
            for i in range(4):
                entry = f.read(16)
                if entry[4] != 0:
                    start = int.from_bytes(entry[8:12], byteorder='little')
                    size = int.from_bytes(entry[12:16], byteorder='little')
                    partition_type = entry[4]
                    partition_types = {
                        0x00: "Unused",
                        0x07: "NTFS",
                        0x0B: "FAT32",
                        0x0C: "FAT32",
                    }
                    partition_type_str = partition_types.get(partition_type, "Unknown")
                    print(f"Partition {i+1} starting offset: {start*512} bytes, size: {size*512/1024/1024} mega bytes, type: {partition_type_str}")	

        