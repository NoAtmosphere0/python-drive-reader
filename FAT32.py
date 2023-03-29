class FAT32:
    def __init__(self)->None:
        #Boot Sector FAT32
        self.BPB_BytesPerSec = 0 #2 bytes
        self.BPB_SecPerClus = 0 #1 byte
        self.BPB_RsvdSecCnt = 0 #2 bytes
        self.BPB_NumFATs = 0 #1 byte
        self.BPB_totSec32 = 0 #4 bytes
        self.BPB_SecsPerFAT = 0 #4 bytes
        self.BPB_RootClus = 0 #4 bytes
        self.BPB_FSInfo = 0 #8 bytes
        #primary entry
        self.PE_status = 0 #1 byte
        self
    def readBootSector(self, drive):
        with open(drive, 'rb') as fp:
            fp.read(11)
            self.BPB_BytesPerSec = int.from_bytes(fp.read(2), byteorder='little')
            self.BPB_SecPerClus = int.from_bytes(fp.read(1), byteorder='little')
            self.BPB_RsvdSecCnt = int.from_bytes(fp.read(2), byteorder='little')
            self.BPB_NumFATs = int.from_bytes(fp.read(1), byteorder='little')
            fp.seek(15,1)
            self.BPB_totSec32 = int.from_bytes(fp.read(4), byteorder='little')
            self.BPB_SecsPerFAT = int.from_bytes(fp.read(4), byteorder='little')
            fp.seek(4,1)
            self.BPB_RootClus = int.from_bytes(fp.read(4), byteorder='little')
            fp.seek(34,1)
            self.BPB_FSInfo = fp.read(8).decode('utf-8')
        return 0
    def printBootSector(self):
        print("Bytes per sector: ", self.BPB_BytesPerSec)
        print("Sectors per cluster: ", self.BPB_SecPerClus)
        print("Reserved sectors: ", self.BPB_RsvdSecCnt)
        print("Number of FATs: ", self.BPB_NumFATs)
        print("Total sectors: ", self.BPB_totSec32)
        print("Sectors per FAT: ", self.BPB_SecsPerFAT)
        print("Root cluster: ", self.BPB_RootClus)
        print("FSInfo: ", self.BPB_FSInfo)
        return 0

#bst = FAT32()
#read from FAT32 partition
#bst.readBootSector(r"C:\Users\pkhoa\Documents\Operating System\Partition data-20230316T151812Z-001\Partition data\bin_FAT32_Partition2.bin")

