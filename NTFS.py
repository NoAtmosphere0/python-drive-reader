""""This file contains the NTFS class
    which is used to read the NTFS file system
    and extract the information from it."""
import datetime

def two_complement(value, bits): # Converts a two's complement number to a decimal
    if value & (1 << (bits - 1)) != 0:
        value = value - (1 << bits)
    return value
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

        self.entries = [] # A dictionary of all the entries in the MFT

        self.drive_path = drive
        self._readVBR()
    
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


    def _readVBR(self):
        with open(self.drive_path, 'rb') as f:
            # Read the VBR (first sector of the partition)
            f.seek(self.starting_offset)
            vbr_data = f.read(512)

            # Parse the VBR to extract key information
            self.bytes_per_sector = int.from_bytes(vbr_data[11:13], byteorder='little')

            self.sectors_per_cluster = int.from_bytes(vbr_data[13:14], byteorder='little')

            self.mft_start_cluster = int.from_bytes(vbr_data[48:56], byteorder='little')
            print(f"MFT start cluster: {self.mft_start_cluster}")

            self.mft_offset = self.starting_offset + (self.mft_start_cluster * self.bytes_per_sector * self.sectors_per_cluster)
            print(f"MFT offset: {self.mft_offset}")
            
            
            self.mft_record_size = int.from_bytes(vbr_data[0x40:0x44], byteorder='little') * self.bytes_per_sector
            
            print(f"MFT record size: {self.mft_record_size}")	
        
        self.readMFT()

    def readMFT(self):
        with open(self.drive_path, 'rb') as f:
            # Read the MFT
            f.seek(self.mft_offset)
            current_entry = self.mft_offset
            while True:
                entry = f.read(self.mft_record_size)
                if entry[0:4] != b"FILE" and entry[0:4] != b"BAAD": # If the entry is not a file or a bad entry,
                    break
                entry_dict = self.readEntry(current_entry)
                current_entry += self.mft_record_size
                self.entries.append(entry_dict)

    def readEntry(self, entry_offset):
        with open(self.drive_path, 'rb') as f:
            f.seek(entry_offset)
            entry = f.read(self.mft_record_size)
            
            if entry[0:4] != b"FILE" and entry[0:4] != b"BAAD":
                return None
            
            entry_dict = {}
            entry_dict["type"] = "FILE"
            entry_dict["size"] = int.from_bytes(entry[48:56], byteorder='little', signed=True)
            entry_dict["created_time"] = self.convert_time(int.from_bytes(entry[24:32], byteorder='little', signed=False))
            entry_dict["modified_time"] = self.convert_time(int.from_bytes(entry[16:24], byteorder='little', signed=False))
            entry_dict["accessed_time"] = self.convert_time(int.from_bytes(entry[8:16], byteorder='little', signed=False))
            
            # Get the filename from the FILE_NAME attribute
            attribute_offset = int.from_bytes(entry[20:22], byteorder='little')
            while attribute_offset != 0:
                attribute = entry[attribute_offset:]
                attribute_type = int.from_bytes(attribute[0:4], byteorder='little')
                
                if attribute_type == 0x30: # FILE_NAME attribute
                    attribute_content_offset = int.from_bytes(attribute[20:22], byteorder='little')
                    attribute_content = attribute[attribute_content_offset:]
                    filename_len = int.from_bytes(attribute_content[64:65], byteorder='little')
                    filename = attribute_content[66:66+filename_len].decode("utf-16")
                    entry_dict["filename"] = filename
                    break
                    
                attribute_offset = int.from_bytes(attribute[4:6], byteorder='little')
            
            if "filename" not in entry_dict:
                entry_dict["filename"] = "N/A"
            
            return entry_dict



    def convert_time(self, time_int):
        # Convert a 64-bit Windows FILETIME value to a Python datetime object
        epoch = datetime.datetime(1650, 1, 1)
        seconds = time_int / 100 /1000 /1000
        unix_time = epoch + datetime.timedelta(seconds=seconds)
        return unix_time.strftime("%d/%m/%Y %H:%M:%S")

    def print_entries(self):
        for entry in self.entries:
            print(entry)     
        print(f"Number of entries: {len(self.entries)}")	
    

        

    
         