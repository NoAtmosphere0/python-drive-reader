""""This file contains the NTFS class
    which is used to read the NTFS file system
    and extract the information from it."""

class NTFS:
    def __init__(self, starting_offset) -> None:
        self.size = 0
        self.starting_offset = starting_offset
        self.sector_size = 0
        self.cluster_size = 0
        self.cluster_per_sector = 0
        self.mft_starting_cluster = 0
        self.mft_record_size = 0
        self.mft_record_per_cluster = 0
        self.mft_record_per_sector = 0
    
    def get_size(self, drive):
        with open(drive, 'rb') as f:
            f.seek(self.starting_offset + 0x18)
            self.size = int.from_bytes(f.read(8), byteorder='little')
            return self.size
    
    
         