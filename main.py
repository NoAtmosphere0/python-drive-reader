import NTFS 
import disk_info 
import GUI
import FAT32

def main():
    ntfs_path = r"C:\Users\pkhoa\Documents\Operating System\Partition data-20230316T151812Z-001\Partition data\bin_NTFS_Partition1.bin" 
    fat32_path = r"C:\Users\pkhoa\Documents\Operating System\Partition data-20230316T151812Z-001\Partition data\bin_FAT32_Partition2.bin"
    disk_info_path = r"C:\Users\pkhoa\Documents\Operating System\Partition data-20230316T151812Z-001\Partition data\bin_disk_information.bin"
    #! This path should be PhysicalDrive1 in the final version

    # master_boot_record = disk_info.MBR(drive)
    # master_boot_record.printMBR()

    """"Testing the partition table class"""
    pt = disk_info.partition_table()
    pt.readPT(disk_info_path)
    pt.print_partitions()

    # pt.read(drive)

    """"Testing the NTFS class"""
    # ntfs = NTFS.NTFS(0, drive)
    # ntfs.print_size()
    print("Exiting main()")

if (__name__ == "__main__"):
    main()

