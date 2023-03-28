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

            # Check if the entry is in use
            if entry[0:4] != b"FILE":
                return None

            entry_dict = {}

            # Determine the entry type
            if entry[0x16:0x18] == b"\x30\x00":
                entry_dict["type"] = "FILE"
            elif entry[0x16:0x18] == b"\x50\x00":
                entry_dict["type"] = "FOLDER"
            else:
                entry_dict["type"] = "UNKNOWN"

            # Get the entry size
            entry_dict["size"] = int.from_bytes(entry[0x30:0x38], byteorder='little', signed=True)

            # Get the created, modified, and accessed times
            entry_dict["created_time"] = self.convert_time(int.from_bytes(entry[0x18:0x20], byteorder='little', signed=False))
            entry_dict["modified_time"] = self.convert_time(int.from_bytes(entry[0x10:0x18], byteorder='little', signed=False))
            entry_dict["accessed_time"] = self.convert_time(int.from_bytes(entry[0x08:0x10], byteorder='little', signed=False))

            # Get the filename attribute
            attribute_offset = self.get_attribute_offset(entry, 0x30)
            if attribute_offset is None:
                entry_dict["filename"] = "N/A"
            else:
                attribute = entry[attribute_offset:]
                attribute_type = int.from_bytes(attribute[0:4], byteorder='little')
                if attribute_type == 0x30:
                    attribute_content_offset = int.from_bytes(attribute[0x14:0x16], byteorder='little')
                    attribute_content = attribute[attribute_content_offset:]
                    filename_len = int.from_bytes(attribute_content[0x40:0x41], byteorder='little')
                    filename = attribute_content[0x42:0x42+filename_len].decode("utf-16")
                    entry_dict["filename"] = filename
                elif attribute_type == 0x50:
                    entry_dict["filename"] = "N/A"
                else:
                    entry_dict["filename"] = "N/A"

            # If the entry is a folder, get the subfolder entries
            if entry_dict["type"] == "FOLDER":
                entry_dict["subentries"] = []
                attribute_offset = self.get_attribute_offset(entry, 0x90)
                if attribute_offset is not None:
                    attribute = entry[attribute_offset:]
                    start_vcn = int.from_bytes(attribute[0x10:0x18], byteorder='little')
                    end_vcn = int.from_bytes(attribute[0x18:0x20], byteorder='little')
                    cluster_size = self.bytes_per_sector * self.sectors_per_cluster
                    for i in range(start_vcn, end_vcn + 1):
                        cluster_offset = self.mft_offset + i * cluster_size
                        for j in range(self.records_per_cluster):
                            entry_offset = cluster_offset + j * self.mft_record_size
                            subentry_dict = self.readEntry(entry_offset)
                            if subentry_dict is not None:
                                entry_dict["subentries"].append(subentry_dict)

            return entry_dict


    def get_attribute_offset(self, entry, attribute_type):
        # Get the offset of the attribute with the specified type
        offset = 0
        while True:
            # Get the attribute header
            attribute_header = entry[offset:offset+16]
            if attribute_header == b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00":
                # This is the end of the attributes, so the attribute was not found
                return None
            # Get the attribute type and length
            attribute_type_found = int.from_bytes(attribute_header[0:4], byteorder='little')
            attribute_length = int.from_bytes(attribute_header[4:8], byteorder='little')
            if attribute_type_found == attribute_type:
                # This is the attribute we were looking for, so return its offset
                return offset
            # Move to the next attribute
            offset += attribute_length
        return None


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
    

        

    
         