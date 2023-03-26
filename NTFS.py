""""This file contains the NTFS class
    which is used to read the NTFS file system
    and extract the information from it."""
import datetime

class NTFS:
    def __init__(self, starting_offset, drive): # Takes the starting offset of the NTFS partition and the drive path
        self.size = 0
        self.starting_offset = starting_offset
        self.bytes_per_sector = None
        self.sectors_per_cluster = None
        self.mft_start_cluster = None
        self.mft_record_size = None
        self.mft_entry_size = None

        self.mft_offset = None # The offset of the MFT        
        self.mft_record = None # The MFT record
        self.mft_header = None # The MFT header
        self.mft_attributes = None # The MFT attributes
        self.clusters_per_mft_record = None # The number of clusters per MFT record

        self.entries = {} # A dictionary of all the entries in the MFT

        self.drive_path = drive
    
    def get_size(self, drive):  # Gets the size of the NTFS partition
        with open(drive, 'rb') as f:
            f.seek(self.starting_offset + 0x18)
            self.size = int.from_bytes(f.read(8), byteorder='little')
            return self.size
        
    def print_size(self): # Prints the size of the NTFS partition
        print(f"Size: {self.size}")

    def print_stats(self): # Prints the statistics of the NTFS partition
        print(f"Bytes per sector: {self.bytes_per_sector}")
        print(f"Sectors per cluster: {self.sectors_per_cluster}")
        print(f"MFT start cluster: {self.mft_start_cluster}")
        print(f"MFT record size: {self.mft_record_size}")
        print(f"MFT record: {self.mft_record}")
        print(f"MFT header: {self.mft_header}")
        print(f"MFT attributes: {self.mft_attributes}")

    def readVBR(self):
        with open(self.drive_path, 'rb') as f:
            # Read the VBR (first sector of the partition)
            vbr_data = f.read(512)

            # Parse the VBR to extract key information
            self.bytes_per_sector = int.from_bytes(vbr_data[11:13], byteorder='little')
            self.sectors_per_cluster = int.from_bytes(vbr_data[13:14], byteorder='little')
            self.mft_start_cluster = int.from_bytes(vbr_data[48:56], byteorder='little')
            self.mft_offset = self.starting_offset + (self.mft_start_cluster * self.bytes_per_sector * self.sectors_per_cluster)

            self.mft_record_size = int.from_bytes(vbr_data[48:50], byteorder='little') * self.bytes_per_sector
            self.clusters_per_mft_record = int.from_bytes(vbr_data[64:66], byteorder='little')
               
    def readMFT(self):
        with open(self.drive_path, 'rb') as f:

            # Read the MFT
            f.seek(self.mft_offset)

            while True:
                entry = f.read(self.mft_record_size)
                if entry[0:4] != b"FILE" and entry[0:4] != b"BAAD:": # If the entry is not a file or a bad entry,
                    break
                entry_dict = {}
                entry_dict["type"] = "FILE"
                entry_dict["size"] = int.from_bytes(entry[48:56], byteorder='little', signed=True)
                entry_dict["created_time"] = self.convert_time(int.from_bytes(entry[24:32], byteorder='little', signed=False))
                entry_dict["modified_time"] = self.convert_time(int.from_bytes(entry[16:24], byteorder='little', signed=False))
                entry_dict["accessed_time"] = self.convert_time(int.from_bytes(entry[8:16], byteorder='little', signed=False))

                # Get the filename from the filename attribute
                attribute_offset = int.from_bytes(entry[20:22], byteorder='little')
                attribute = entry[attribute_offset:]
                attribute_type = int.from_bytes(attribute[0:4], byteorder='little')
                if attribute_type == 0x30:
                    attribute_content_offset = int.from_bytes(attribute[20:22], byteorder='little')
                    attribute_content = attribute[attribute_content_offset:]
                    filename_len = int.from_bytes(attribute_content[64:65], byteorder='little')
                    filename = attribute_content[66:66+filename_len].decode("utf-16")
                    entry_dict["filename"] = filename
                else:
                    entry_dict["filename"] = "N/A"

                # Add the entry to the dictionary
                self.entries[int.from_bytes(entry[0:8], byteorder='little')] = entry_dict
                print(entry_dict)

    def convert_time(self, time_int):
        # Convert a 64-bit Windows FILETIME value to a Python datetime object
        epoch = datetime.datetime(1601, 1, 1)
        seconds = time_int / 10000000
        unix_time = epoch + datetime.timedelta(seconds=seconds)
        return unix_time.strftime("%d/%m/%Y %H:%M:%S")

    def print_entries(self):
        print(self.entries)        
    

        

    
         