""""This file contains the NTFS class
    which is used to read the NTFS file system
    and extract the information from it."""
import datetime
import struct

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

        self.entries = {} # A dictionary of all the entries in the MFT

        self.drive_path = drive
        self._readVBR()
    

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
            f.read(self.starting_offset)
            vbr_data = f.read(512)

            # Parse the VBR to extract key information
            self.bytes_per_sector = int.from_bytes(vbr_data[11:13], byteorder='little')

            self.sectors_per_cluster = int.from_bytes(vbr_data[13:14], byteorder='little')

            self.mft_start_cluster = int.from_bytes(vbr_data[48:56], byteorder='little')
            print(f"MFT start cluster: {self.mft_start_cluster}")

            self.mft_offset = self.starting_offset + (self.mft_start_cluster * self.bytes_per_sector * self.sectors_per_cluster)
            print(f"MFT offset: {self.mft_offset}")
            
            
            self.mft_record_size = int.from_bytes(vbr_data[0x40:0x41], byteorder='little') * self.bytes_per_sector
            
            print(f"MFT record size: {self.mft_record_size}")	
        
        self.readMFT()

    def change_index(self, dict):
        new_order = ["type", "size", "created", "modified"] 
        new_dict = {key: dict[key] for key in new_order}

        return new_dict       

    def readMFT(self):
        with open(self.drive_path, 'rb') as f:
            # Read the MFT
            f.read(self.mft_offset)
            #f.read(self.mft_record_size)
            while True:
                entry = f.read(self.mft_record_size)
                if entry[0:4] != b"FILE" and entry[0:4] != b"BAAD": # If the entry is not a file or a bad entry,
                    break
                entry_dict = self.readEntry(entry)
                if (len(entry_dict) == 5):
                    filename = entry_dict["name"]
                    entry_dict = self.change_index(entry_dict)
                    
                    self.entries[filename] = entry_dict
                else:
                    continue
                

    def readEntry(self, entry):
        entry_dict = {}

        entry_header = entry[0:48]
        attribute_offset = int.from_bytes(entry_header[0x14:0x16], byteorder='little')
        attributes = entry[attribute_offset:]

        current = 0
        while (attributes[current + 0x00:current + 0x04] != b"\xFF\xFF\xFF\xFF"):
    
            attribute_header = attributes[current:current + 0x0F]
            attribute_length = int.from_bytes(attribute_header[0x04:0x08], byteorder='little')
            attribute_type = int.from_bytes(attribute_header[0x00:0x04], byteorder='little')
            resident_flag = int.from_bytes(attribute_header[0x08:0x09], byteorder='little')

            attribute_content_size = int.from_bytes(attributes[0x10:0x13], byteorder='little')
            attribute_content_offset = int.from_bytes(attributes[0x14:0x15], byteorder='little')


            if attribute_type == 0x10 or attribute_type == 16: # Standard Information
                attribute_content = attributes[current + attribute_content_offset:current + attribute_content_offset + attribute_content_size]
                created = attribute_content[0x00:0x08]
                modified = attribute_content[0x08:0x16]
                entry_dict["created"] = self.convert_time(struct.unpack("<Q", created)[0])
                entry_dict["modified"] = self.convert_time(struct.unpack("<Q", attribute_content[8:16])[0])

            elif attribute_type == 0x30 or attribute_type == 48: # File Name
                attribute_content = attributes[current + attribute_content_offset:current + attribute_content_offset + attribute_content_size * 2]
                
                attribute_flag = attribute_content[0x38:0x42]
                attribute_flag = int.from_bytes(attribute_flag, byteorder='little')
                attribute_flag = bin(attribute_flag)
                attribute_flag = attribute_flag[::-1]
                
                if attribute_flag[5] == '1':
                    entry_dict["type"] = "FILE"
                
                if attribute_flag[28] == '1':
                    entry_dict["type"] = "FOLDER"

                if attribute_flag[2] == '1':
                    entry_dict["type"] = "SYSTEM"

                name_length = int.from_bytes(attribute_content[0x40:0x41], byteorder='little')
                entry_dict["name"] = attribute_content[0x42: 0x42 + name_length*2].decode("utf-16")

            # Get the entry size
            elif attribute_type == 0x80 or attribute_type == 128:
                attribute_content = attributes[current + attribute_content_offset:current + attribute_content_offset + attribute_content_size]

                if resident_flag == 0:
                    entry_dict["size"] = attribute_content_size

                else:
                    entry_dict["size"] = int.from_bytes(attributes[current + 0x30: current + 0x38], byteorder='little')
                


            elif attribute_type == 0xFF or attribute_type == 255:
                break

            current += attribute_length

        

       

        # # If the entry is a folder, get the subfolder entries
        # if entry_dict["type"] == "FOLDER":
        #     entry_dict["subentries"] = []
        #     attribute_offset = self.get_attribute_offset(entry, 0x90)
        #     if attribute_offset is not None:
        #         attribute = entry[attribute_offset:]
        #         start_vcn = int.from_bytes(attribute[0x10:0x18], byteorder='little')
        #         end_vcn = int.from_bytes(attribute[0x18:0x20], byteorder='little')
        #         cluster_size = self.bytes_per_sector * self.sectors_per_cluster
        #         for i in range(start_vcn, end_vcn + 1):
        #             cluster_offset = self.mft_offset + i * cluster_size
        #             for j in range(self.records_per_cluster):
        #                 entry_offset = cluster_offset + j * self.mft_record_size
        #                 subentry_dict = self.readEntry(entry_offset)
        #                 if subentry_dict is not None:
        #                     entry_dict["subentries"].append(subentry_dict)

        return entry_dict


    def get_attribute_offset(self, entry, attribute_type):
        # Find the offset of the attribute of the given type in the MFT entry
        offset = 0x18  # Skip the header of the MFT entry
        while offset < len(entry):
            # Check if we have reached the end of the attributes
            if entry[offset:offset+4] == b"\xff\xff\xff\xff":
                break
            
            # Get the attribute type and length
            attr_type = int.from_bytes(entry[offset:offset+4], byteorder="little")
            attr_len = int.from_bytes(entry[offset+4:offset+8], byteorder="little")
            
            if attr_type == attribute_type:
                # Found the attribute
                return offset
            
            # Move to the next attribute
            offset += attr_len
            
        return None
        


    def convert_time(self, windows_timestamp):
        date = datetime.datetime.fromtimestamp((windows_timestamp - 116444736000000000) / 10000000)
        return date.strftime("%Y-%m-%d %H:%M:%S")

    def print_entries(self):
        for entry in self.entries:
            print(entry + ": " + str(self.entries[entry]))     
        print(f"Number of entries: {len(self.entries)}")	

    def get_entries(self):
        return self.entries
    
    def get_entries_text(self):
        with open("data_ntfs.txt", 'w') as f:
            f.write(str(self.entries))
        self.format_data_file()

    def format_data_file(self):
        with open("data_ntfs.txt", 'r') as f:
            text = f.read().replace("'", '"')
        with open("data_ntfs.txt", 'w') as f:
            f.write(text)
            

        

    
         