import NTFS 
import disk_info 
import GUI
import FAT32

def main():

    ntfs_path = r"bin_files\bin_NTFS_Partition1.bin" 
    fat32_path = r"bin_files\bin_FAT32_Partition2.bin"
    disk_info_path = r"bin_files\bin_disk_information.bin"
    physical_drive = r"\\.\PhysicalDrive1"
    #! This path should be PhysicalDrive1 in the final version

    # master_boot_record = disk_info.MBR(drive)
    # master_boot_record.printMBR()

    """"Testing the partition table class"""
    pt = disk_info.MBR(disk_info_path)

    """"Testing the NTFS class"""
    ntfs = NTFS.NTFS(0, ntfs_path)
    ntfs.readMFT()
    
    #ntfs.print_entries()

    print("Exiting main()")

if (__name__ == "__main__"):
    main()

