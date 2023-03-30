import NTFS
import disk_info

# import FAT32
import GUI


def main():
    ntfs_path = r"bin_files\bin_NTFS_Partition1.bin"
    fat32_path = r"bin_files\bin_FAT32_Partition2.bin"
    disk_info_path = r"bin_files\bin_disk_information.bin"
    physical_drive = r"\\.\PhysicalDrive1"
    #! This path should be PhysicalDrive1 in the final version

    """"Testing the partition table class"""
    pt = disk_info.MBR(physical_drive)
    info_dict = pt.getInfoDict()
    pt.printMBR()
    print(info_dict)

    """"Testing the NTFS class"""
    # ntfs = NTFS.NTFS(0, ntfs_path)

    # ntfs.print_entries()

    print("Exiting main()")


if __name__ == "__main__":
    main()
