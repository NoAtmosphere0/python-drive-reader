import datetime
import struct
import time

class FAT32:
    def __init__(self, starting_offset, drive)->None:
        self.drive_path = drive
        self.info_dict = {}
        self.starting_offset = starting_offset
        self.byte = 0
        #Boot Sector FAT32
        self.BPB_BytesPerSec = 0 #2 bytes
        self.BPB_SecPerClus = 0 #1 byte
        self.BPB_RsvdSecCnt = 0 #2 bytes
        self.BPB_NumFATs = 0 #1 byte
        self.BPB_totSec32 = 0 #4 bytes
        self.BPB_SecsPerFAT = 0 #4 bytes
        self.BPB_RootClus = 0 #4 bytes
        #Entry FAT32
        self.DIR_Name = '' #11 bytes
        self.DIR_Attr = 'type' #1 byte
        self.DIR_CrtTime = '' #2 bytes
        self.DIR_CrtDate = '' #2 bytes
        self.DIR_DateCrt = 'Date Created'
        self.DIR_DateMod = 'Date Modified'
        self.DIR_FileSize = 0 #4 bytes
        self.DIR_CurClus = 0 #4 bytes
        self.DIR_NxtClus = 0 #4 bytes
    
    def readBootSector(self)->None:
        with open(self.drive_path, 'rb') as f:
            self.byte = f.read(512)
            self.BPB_BytesPerSec = int.from_bytes(self.byte[11:13], byteorder='little') 
            self.BPB_SecPerClus = int.from_bytes(self.byte[13:14], byteorder='little') 
            self.BPB_RsvdSecCnt = int.from_bytes(self.byte[14:16], byteorder='little')
            self.BPB_NumFATs = int.from_bytes(self.byte[16:17], byteorder='little')
            self.BPB_HiddSec = int.from_bytes(self.byte[28:32], byteorder='little')
            self.BPB_totSec32 = int.from_bytes(self.byte[32:36], byteorder='little')
            self.BPB_SecsPerFAT = int.from_bytes(self.byte[36:40], byteorder='little')
            self.BPB_RootClus = int.from_bytes(self.byte[44:48], byteorder='little')
            self.BPB_FSInfo = int.from_bytes(self.byte[48:52], byteorder='little')

    def detectDIR(self, offset:hex, startingOffset, root):
        with open(self.drive_path, 'rb') as f:
            f.seek(offset)
            self.byte = f.read(512)
            number = 0
            sub = {}
            for i in range (startingOffset, 512, 32):
                if (self.byte[i] == 0xE5 or self.byte[i] == 0x00):
                    continue
                else:
                    tempData = {}
                    if (self.byte[i+11] == 0x10): #Directory
                        self.DIR_Name = ''
                        j = i + 11
                        if (self.byte[j - 32] == 0x0F):
                            j -= 32
                            subEntry = 1
                            temp = 32
                            while (self.byte[j - temp] == 0x0F):
                                temp += 32
                                subEntry += 1
                            for t in range(0, subEntry, 1):
                                check = True
                                temp = ''
                                index = t * 32
                                while check:
                                    for k in range(10, 0, -2):
                                        if (
                                            (self.byte[j - k - index] == 0x00 and self.byte[j - k + 2 - index] == 0xFF) 
                                            or (self.byte[j - k - index] == 0x00 and self.byte[j - k + 2 - index] == 0x00)
                                            or (self.byte[j - k - index] == 0xFF and self.byte[j - k + 2 - index] == 0xFF)
                                        ):
                                            check = False
                                            break
                                        temp += (self.byte[j - k - index:j - k + 2 - index]).decode('utf-8')
                                    for k in range(3, 14, 2):
                                        if (
                                            (self.byte[j + k - index] == 0x00 and self.byte[j + k + 2 - index] == 0xFF) 
                                            or (self.byte[j + k - index] == 0x00 and self.byte[j + k + 2 - index] == 0x00)
                                            or (self.byte[j + k - index] == 0xFF and self.byte[j + k  + 2- index] == 0xFF)
                                        ):
                                            check = False
                                            break
                                        temp += (self.byte[j + k - index:j + k + 2 - index]).decode('utf-8')
                                    for k in range(17, 20, 2):
                                        if (
                                            (self.byte[j + k - index] == 0x00 and self.byte[j + k + 2 - index] == 0xFF) 
                                            or (self.byte[j + k - index] == 0x00 and self.byte[j + k + 2 - index] == 0x00)
                                            or (self.byte[j + k - index] == 0xFF and self.byte[j + k  + 2- index] == 0xFF)
                                        ):
                                            check = False
                                            break
                                        temp += (self.byte[j + k - index:j + k + 2 - index]).decode('utf-8')
                                    check = False
                                self.DIR_Name += temp           
                        else:
                            self.DIR_Name = (self.byte[i:i+8]).decode('utf-8').rstrip()
                        #created time
                        temp = self.byte[i+13:i+16]
                        reversed_temp = temp[::-1]
                        binary_string = ''.join(f'{byte:08b}' for byte in reversed_temp)
                        int_value = int(binary_string, 2)
                        hours = int_value >> 19
                        minutes = (int_value >> 13) & 0x3F
                        seconds = (int_value >> 7) & 0x3F
                        milliseconds = int_value & 0x7F
                        self.DIR_CrtTime = datetime.time(hours, minutes, seconds, milliseconds * 10000)
                        self.DIR_CrtTime = self.DIR_CrtTime.strftime('%H:%M:%S')
                        ################
                        #created date
                        temp = self.byte[i+16:i+18]
                        reversed_temp = temp[::-1]
                        binary_string = ''.join(f'{byte:08b}' for byte in reversed_temp)
                        int_value = int(binary_string, 2)
                        year = 1980 + (int_value >> 9)
                        month = (int_value >> 5) & 0x0F
                        day = int_value & 0x1F
                        self.DIR_CrtDate = datetime.date(year, month, day)
                        self.DIR_CrtDate = self.DIR_CrtDate.strftime('%m/%d/%Y') #converted to mdy
                        ################
                        #next cluster
                        temp = self.byte[i+26:i+27]
                        binary_string = ''.join(f'{byte:08b}' for byte in temp)
                        int_value = int(binary_string, 2)
                        self.DIR_NxtClus = int_value
                        ################
                        tempData['name'] = self.DIR_Name
                        tempData['type'] = 'folder'
                        tempData['created'] = self.DIR_CrtDate + ' ' + self.DIR_CrtTime
                        tempData['modified'] = None
                        if (self.DIR_NxtClus != 0):
                            tempData.update({
                                'contents' : 
                                self.detectDIR(
                                            offset + (self.DIR_NxtClus - root) * self.BPB_BytesPerSec * self.BPB_SecPerClus, 
                                            64, self.DIR_NxtClus)
                                            })
                            if (tempData['contents'] == {}):
                                tempData.update({'contents' : None})
                        else:
                            tempData.update({'contents' : None})
                            return
                        sub.update({number:tempData})
                        number += 1
                    elif (self.byte[i+11] == 0x20): #File
                        self.DIR_Name = ''
                        j = i + 11
                        if (self.byte[j - 32] == 0x0F):
                            j -= 32
                            subEntry = 1
                            temp = 32
                            while (self.byte[j - temp] == 0x0F):
                                temp += 32
                                subEntry += 1
                            for t in range(0, subEntry, 1):
                                check = True
                                temp = ''
                                index = t * 32
                                while check:
                                    for k in range(10, 0, -2):
                                        if (
                                            (self.byte[j - k - index] == 0x00 and self.byte[j - k + 2 - index] == 0xFF) 
                                            or (self.byte[j - k - index] == 0x00 and self.byte[j - k + 2 - index] == 0x00)
                                            or (self.byte[j - k - index] == 0xFF and self.byte[j - k + 2 - index] == 0xFF)
                                        ):
                                            check = False
                                            break
                                        temp += (self.byte[j - k - index:j - k + 2 - index]).decode('utf-8')
                                    for k in range(3, 14, 2):
                                        if (
                                            (self.byte[j + k - index] == 0x00 and self.byte[j + k + 2 - index] == 0xFF) 
                                            or (self.byte[j + k - index] == 0x00 and self.byte[j + k + 2 - index] == 0x00)
                                            or (self.byte[j + k - index] == 0xFF and self.byte[j + k  + 2- index] == 0xFF)
                                        ):
                                            check = False
                                            break
                                        temp += (self.byte[j + k - index:j + k + 2 - index]).decode('utf-8')
                                    for k in range(17, 20, 2):
                                        if (
                                            (self.byte[j + k - index] == 0x00 and self.byte[j + k + 2 - index] == 0xFF) 
                                            or (self.byte[j + k - index] == 0x00 and self.byte[j + k + 2 - index] == 0x00)
                                            or (self.byte[j + k - index] == 0xFF and self.byte[j + k  + 2- index] == 0xFF)
                                        ):
                                            check = False
                                            break
                                        temp += (self.byte[j + k - index:j + k + 2 - index]).decode('utf-8')
                                    check = False
                                self.DIR_Name += temp                          
                        else:
                            self.DIR_Name = (self.byte[i:i+8]).decode('utf-8').rstrip() + '.' + (self.byte[i+8:i+11]).decode('utf-8')
                        self.DIR_Attr = 'File'
                        #created time
                        temp = self.byte[i+13:i+16]
                        reversed_temp = temp[::-1]
                        binary_string = ''.join(f'{byte:08b}' for byte in reversed_temp)
                        int_value = int(binary_string, 2)
                        hours = int_value >> 19
                        minutes = (int_value >> 13) & 0x3F
                        seconds = (int_value >> 7) & 0x3F
                        milliseconds = int_value & 0x7F
                        self.DIR_CrtTime = datetime.time(hours, minutes, seconds, milliseconds * 10000)
                        self.DIR_CrtTime = self.DIR_CrtTime.strftime('%H:%M:%S')
                        ################
                        #created date
                        temp = self.byte[i+16:i+18]
                        reversed_temp = temp[::-1]
                        binary_string = ''.join(f'{byte:08b}' for byte in reversed_temp)
                        int_value = int(binary_string, 2)
                        year = 1980 + (int_value >> 9)
                        month = (int_value >> 5) & 0x0F
                        day = int_value & 0x1F
                        self.DIR_CrtDate = datetime.date(year, month, day)
                        self.DIR_CrtDate = self.DIR_CrtDate.strftime('%m/%d/%Y') #converted to mdy
                        ################'
                        #file size
                        temp = self.byte[i+28:i+32]
                        reversed_temp = temp[::-1]
                        binary_string = ''.join(f'{byte:08b}' for byte in reversed_temp)
                        int_value = int(binary_string, 2)
                        self.DIR_FileSize = int_value
                        ################
                        tempData['name'] = self.DIR_Name
                        tempData['type'] = 'file'
                        tempData['created'] = self.DIR_CrtDate + ' ' + self.DIR_CrtTime
                        tempData['modified'] = None
                        tempData['size'] = self.DIR_FileSize
                        sub.update({number:tempData})
                        number += 1
                    else:
                        continue
                    # self.info_dict.update({number: tempData})
                    # number = number + 1
        return sub
    def FindDirectory(self, offset:hex, Cluster:hex)->None:
        if (Cluster == 0x2):
            for i in range(0, len(self.detectDIR(offset, 128, self.BPB_RootClus)), 1):
                self.info_dict.update({i: self.detectDIR(offset, 128, self.BPB_RootClus)[i]})

    def getEntry(self)->None:
        return self.info_dict
    def getBootSector(self):
        temp_dict = {
                'StartingOffset': self.starting_offset,
                'BPB_BytesPerSec': self.BPB_BytesPerSec,
                'BPB_SecPerClus': self.BPB_SecPerClus,
                'BPB_RsvdSecCnt': self.BPB_RsvdSecCnt,
                'BPB_NumFATs': self.BPB_NumFATs,
                'BPB_TotSec32': self.BPB_totSec32,
                'BPB_SecsPerFAT':self.BPB_SecsPerFAT,
                'BPB_RootClus': self.BPB_RootClus,
                }
        return temp_dict
    

#####################
DRIVE = FAT32(0, '\\\\.\G:') #change the drive letter here

DRIVE.readBootSector() #read the boot sector -> get the starting offset. Noted this is the compulsary step

RDET = (
        DRIVE.getBootSector()['BPB_RsvdSecCnt'] +           
        DRIVE.getBootSector()['BPB_NumFATs'] *              #calculate the Root Directory Entry Table
        DRIVE.getBootSector()['BPB_SecsPerFAT'] +           #RDET = Reserved Sector Count + Number of FATs * Sectors per FAT + Starting Offset
        DRIVE.getBootSector()['StartingOffset']             #RDET in FAT32 is stored in the root directory
        ) * DRIVE.getBootSector()['BPB_BytesPerSec'] 

DRIVE.FindDirectory(RDET, DRIVE.getBootSector()['BPB_RootClus']) #find the directory of FAT32 drive

DATA = DRIVE.getEntry() #get the data of the directory

print(DATA) #print the data in dictionary format