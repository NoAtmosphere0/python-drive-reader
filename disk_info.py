""""This file contains the MBR and partition table class
    which is used to read and extract information the MBR and partition table"""

# TODO: Create function(s) to parse the MBR
# TODO: and determine the number of partition tables and their styles
""""Which includes: total number of partitions, their types, and their sizes and 
    locations on the disk."""


class NoDiskFound(Exception):
    pass


class MBR:
    def __init__(self, drive) -> None:
        self.drive = drive
        self.data = None
        self.status = None
        self.partition_type = None
        self.starting_sector = None
        self.total_sectors = None
        self.offset = 0x1BE
        self.size = 0x10
        self.partitions = {}

        self.info_dict = {}

        try:
            with open(drive, "rb") as mbr:
                self.data = mbr.read(446)
                self.status = hex(int.from_bytes(self.data[0:1], byteorder="little"))
                self.partition_type = hex(
                    int.from_bytes(self.data[4:5], byteorder="little")
                )
                self.starting_sector = int.from_bytes(
                    self.data[8:12], byteorder="little"
                )
                self.total_sectors = int.from_bytes(
                    self.data[12:16], byteorder="little"
                )
        except FileNotFoundError:
            raise NoDiskFound("No disk found at specified drive location.")

        self._readPT()
        self._loadInfo()

    def printMBR(
        self,
    ):  # Prints the MBR data such as the status, partition type, starting sector, and total sectors
        print("MBR data: ")
        print("Status: ", self.status)
        print("Partition type: ", self.partition_type)
        print("Starting sector: ", self.starting_sector)
        print("Total sectors: ", self.total_sectors)
        print("----------------------------------")

    # returns disk information as a dictionary
    def getInfo(self):
        return self.info_dict

    # loads information into the dictionary
    def _loadInfo(self):
        self.info_dict["partition_type"] = self.partition_type
        self.info_dict["starting_sector"] = self.starting_sector
        self.info_dict["total_sectors"] = self.total_sectors
        self.info_dict["partitions"] = self.partitions

    def _readPT(self):  # Reads the partition table
        with open(self.drive, "rb") as f:
            f.read(446)
            for _ in range(2):
                entry = f.read(16)
                if entry[4] != 0:
                    start = int.from_bytes(entry[8:12], byteorder="little")
                    size = int.from_bytes(entry[12:16], byteorder="little")
                    partition_type = entry[4]
                    partition_types = {
                        0x00: "Unused",
                        0x07: "NTFS",
                        0x0B: "FAT32",
                        0x0C: "FAT32",
                    }
                    partition_type_str = partition_types.get(partition_type, "Unknown")
                    # print(f"Partition {i+1} starting offset: {start*512} bytes, size: {size*512/1024/1024} mega bytes, type: {partition_type_str}")
                    self.partitions[partition_type_str] = [start * 512, size * 512]

    def getInfoDict(self):
        return self.info_dict

    def print_partitions(self):  # Prints the partition table
        print("Partition table data: ")
        for i in self.partitions:
            print(
                f"Partition type: {i}, starting offset: {self.partitions[i][0]} bytes, size: {self.partitions[i][1] / 1024 / 1024} mega bytes"
            )
        print("----------------------------------")

    def get_partitions(self):
        return self.partitions
