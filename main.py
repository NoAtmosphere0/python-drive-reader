import NTFS
import disk_info

import FAT32
import GUI
#import GUI_demo

"""{'partition_type': '0xbc', 
    'starting_sector': 525338448, 
    'Disk size': '992.8670635223389 MB', 
    'partitions': {
        'NTFS': [65536, 536870912], 
        'FAT32': [536936448, 536870912]
        }   
    }"""

def main():
    ntfs_path = r"bin_files\bin_NTFS_Partition1.bin"
    fat32_path = r"bin_files\bin_FAT32_Partition2.bin"
    disk_info_path = r"bin_files\bin_disk_information.bin"
    physical_fat32 = r"\\.\Physicalfat321"
    #! This path should be Physicalfat321 in the final version

    """"Testing the partition table class"""
    pt = disk_info.MBR(disk_info_path)
    info_dict = pt.getInfoDict()
    pt.printMBR()
    print(info_dict)

    """"Testing the NTFS class"""
    ntfs = NTFS.NTFS(0, ntfs_path)
    ntfs.get_entries_text()
    #ntfs.print_entries()
    #print(ntfs.get_entries())
    
    
    fat32 = FAT32.FAT32(0, fat32_path)
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

    GUI.main()
    print("Exiting main()")


if __name__ == "__main__":
    main()
