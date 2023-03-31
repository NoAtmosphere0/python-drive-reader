import NTFS
import disk_info
import FAT32
import GUI

def main():
    physical_drive = r"\\.\PhysicalDrive1"  

    print("Reading the physical drive....")

    """"MBR class"""
    pt = disk_info.MBR(physical_drive)
    ntfs_offset, fat32_offset = pt.get_partitions_offset()

    print("FAT32 offset: ", fat32_offset)
    print("NTFS offset: ", ntfs_offset)

    """"NTFS class"""
    ntfs = NTFS.NTFS(ntfs_offset, physical_drive)
    ntfs.get_entries_text()

    
    """"FAT32 class"""
    fat32 = FAT32.FAT32(fat32_offset, physical_drive)
    fat32.readBootSector()
    RDET = (
        fat32.getBootSector()['BPB_RsvdSecCnt'] +           
        fat32.getBootSector()['BPB_NumFATs'] *              #calculate the Root Directory Entry Table
        fat32.getBootSector()['BPB_SecsPerFAT'] +           #RDET = Reserved Sector Count + Number of FATs * Sectors per FAT + Starting Offset
        fat32.getBootSector()['StartingOffset']             #RDET in FAT32 is stored in the root directory
        ) * fat32.getBootSector()['BPB_BytesPerSec'] 
    fat32.FindDirectory(RDET) #find the directory of FAT32fat32 
    DATA = fat32.getDATA() #get the data of the directory

    FAT32.print_to_json(FAT32.format_dict(DATA), 'data_fat32.txt') #print the data in json format

    print("Starting GUI")
    GUI.main()
    print("Exiting main()")


if __name__ == "__main__":
    main()
