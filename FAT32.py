import datetime
import struct
import time
import json

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
    
    # def checkLast(self, offset:hex, startingOffset, root):
    #     with open(self.drive_path, 'rb') as f:
    #         f.seek(offset)
    #         self.byte = f.read(512)
    #         for i in range (startingOffset, 512, 1):
    #             if(self.byte[i] != 0x00):
    #                 return False
    #         return True
    
    # def firstNextCluster(self, offset:hex):
    #     with open(self.drive_path, 'rb') as f:
    #         f.seek(offset)
    #         self.byte = f.read(512)
    #         i = 128
    #         while True:
    #             if (i >= 512):
    #                 f.seek(offset + 512)
    #                 self.byte = f.read(512)
    #                 i = 0
    #             if (self.byte[i] == 0xE5 or self.byte[i] == 0x00):
    #                 i = i + 32
    #             else:
    #                 if (self.byte[i+11] == 0x10): #Directory to get the first next cluster
    #                     temp = self.byte[i+26:i+27]
    #                     binary_string = ''.join(f'{byte:08b}' for byte in temp)
    #                     int_value = int(binary_string, 2)
    #                     return int_value
    #                     break
    #                 else:
    #                     i = i + 32     
    
    # def NextCluster(self, offset:hex, startingOffset, root, destination):
    #     with open(self.drive_path, 'rb') as f:
    #         f.seek(offset)
    #         if (destination == 0): 
    #             self.byte = f.read(512)
    #             for i in range (startingOffset, 512, 32):
    #                 if (self.byte[i] == 0xE5 or self.byte[i] == 0x00):
    #                     continue
    #                 else:
    #                     if (self.byte[i+11] == 0x10): #Directory
    #                         #next cluster
    #                         temp = self.byte[i+26:i+27]
    #                         binary_string = ''.join(f'{byte:08b}' for byte in temp)
    #                         int_value = int(binary_string, 2)
    #         else:
    #             self.byte = f.read((destination - root) * 512)
    #             for i in range (startingOffset, (destination - root) * 512, 32):
    #                 if (self.byte[i] == 0xE5 or self.byte[i] == 0x00):
    #                     continue
    #                 else:
    #                     if (self.byte[i+11] == 0x10): #Directory
    #                         #next cluster
    #                         temp = self.byte[i+26:i+27]
    #                         binary_string = ''.join(f'{byte:08b}' for byte in temp)
    #                         int_value = int(binary_string, 2)
    #         return int_value
    
    def detectFile(self, offset:hex, startingOffset, root):
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
                    if (self.byte[i+11] == 0x20): #File
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
                                        temp += (self.byte[j - k - index:j - k + 1 - index]).decode('utf-8')
                                    for k in range(3, 14, 2):
                                        if (
                                            (self.byte[j + k - index] == 0x00 and self.byte[j + k + 2 - index] == 0xFF) 
                                            or (self.byte[j + k - index] == 0x00 and self.byte[j + k + 2 - index] == 0x00)
                                            or (self.byte[j + k - index] == 0xFF and self.byte[j + k  + 2- index] == 0xFF)
                                        ):
                                            check = False
                                            break
                                        temp += (self.byte[j + k - index:j + k + 1 - index]).decode('utf-8')
                                    for k in range(17, 20, 2):
                                        if (
                                            (self.byte[j + k - index] == 0x00 and self.byte[j + k + 2 - index] == 0xFF) 
                                            or (self.byte[j + k - index] == 0x00 and self.byte[j + k + 2 - index] == 0x00)
                                            or (self.byte[j + k - index] == 0xFF and self.byte[j + k  + 2- index] == 0xFF)
                                        ):
                                            check = False
                                            break
                                        temp += (self.byte[j + k - index:j + k + 1 - index]).decode('utf-8')
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
                        self.DIR_CrtTime = datetime.time(hours, minutes, seconds, milliseconds * 1000)
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
        return sub
    
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
                                        temp += (self.byte[j - k - index:j - k + 1 - index]).decode('utf-8')
                                    for k in range(3, 14, 2):
                                        if (
                                            (self.byte[j + k - index] == 0x00 and self.byte[j + k + 2 - index] == 0xFF) 
                                            or (self.byte[j + k - index] == 0x00 and self.byte[j + k + 2 - index] == 0x00)
                                            or (self.byte[j + k - index] == 0xFF and self.byte[j + k  + 2- index] == 0xFF)
                                        ):
                                            check = False
                                            break
                                        temp += (self.byte[j + k - index:j + k + 1 - index]).decode('utf-8')
                                    for k in range(17, 20, 2):
                                        if (
                                            (self.byte[j + k - index] == 0x00 and self.byte[j + k + 2 - index] == 0xFF) 
                                            or (self.byte[j + k - index] == 0x00 and self.byte[j + k + 2 - index] == 0x00)
                                            or (self.byte[j + k - index] == 0xFF and self.byte[j + k  + 2- index] == 0xFF)
                                        ):
                                            check = False
                                            break
                                        temp += (self.byte[j + k - index:j + k + 1 - index]).decode('utf-8')
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
                        self.DIR_CrtTime = datetime.time(hours, minutes, seconds, milliseconds * 1000)
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
                        NxtClus = int_value
                        # check = self.checkLast(offset + (self.DIR_NxtClus - root) * self.BPB_BytesPerSec * self.BPB_SecPerClus, startingOffset, self.DIR_NxtClus)
                        ################
                        tempData['name'] = self.DIR_Name
                        tempData['type'] = 'folder'
                        tempData['created'] = self.DIR_CrtDate + ' ' + self.DIR_CrtTime
                        tempData['modified'] = None
                        tempData['size'] = None
                        tempData.update({
                            'contents' : 
                            self.detectROOT(
                                offset + (NxtClus - root) * self.BPB_BytesPerSec * self.BPB_SecPerClus, 
                                64, NxtClus)})
                        if (tempData['contents'] == {}): tempData['contents'] = None 
                        sub.update({number:tempData})
                        number += 1
                    else:
                        continue
        return sub
    
    def detectROOT(self, offset:hex, startingOffset, root):
        sub = {}
        t1 = 0
        while t1 < len(self.detectFile(offset, startingOffset, root)):
            sub.update({t1:self.detectFile(offset, startingOffset, root)[t1]})
            t1 += 1
        t2 = 0
        while t2 < len(self.detectDIR(offset, startingOffset, root)):
            t3 = t1 + t2
            sub.update({t3:self.detectDIR(offset, startingOffset, root)[t2]})
            t2 += 1
        return sub

    def FindDirectory(self, offset:hex)->None:
        for i in range(0, len(self.detectROOT(offset, 128, self.BPB_RootClus)), 1):
                self.info_dict.update({i: self.detectROOT(offset, 128, self.BPB_RootClus)[i]})
    
    def getDATA(self)->None:
        temp = self.info_dict
        
        return temp
    
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

def print_data_to_file(data, filename): 
    with open(filename, 'w') as file:
        for key, value in data.items():
            file.write(f'{key}: ')
            for k, v in value.items():
                if k == 'contents':
                    file.write(f'\n\t{k}: ')
                    if v is None:
                        file.write('Empty')
                    else:
                        for ck, cv in v.items():
                            file.write(f'\n\t\t{ck}: ')
                            for ck2, cv2 in cv.items():
                                file.write(f'{ck2}={cv2}, ')
                else:
                    file.write(f'{k}={v}, ')
            file.write('\n\n')
    
def print_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def format_dict(input_dict):
    if input_dict is None:
        return None
    output_dict = {}
    for key, value in input_dict.items():
        name = value["name"]
        del value["name"]
        if value["type"] == "folder":
            contents = value["contents"]
            del value["contents"]
            value["size"] = None
            value["contents"] = format_dict(contents)
            if value["contents"] is None:
                value["contents"] = 'Empty'
        output_dict[name] = value
    #pop size from folders
    for key, value in output_dict.items():
        if value["type"] == "folder":
            value.pop("size", None)
    return output_dict


#####################
DRIVE = FAT32(0, '\\\\.\F:') #change the drive letter here
DRIVE.readBootSector() #read the boot sector -> get the starting offset. Noted this is the compulsary step
#get the next cluster of the cluster number 2
RDET = (
        DRIVE.getBootSector()['BPB_RsvdSecCnt'] +           
        DRIVE.getBootSector()['BPB_NumFATs'] *              #calculate the Root Directory Entry Table
        DRIVE.getBootSector()['BPB_SecsPerFAT'] +           #RDET = Reserved Sector Count + Number of FATs * Sectors per FAT + Starting Offset
        DRIVE.getBootSector()['StartingOffset']             #RDET in FAT32 is stored in the root directory
        ) * DRIVE.getBootSector()['BPB_BytesPerSec'] 
DRIVE.FindDirectory(RDET) #find the directory of FAT32 drive
DATA = DRIVE.getDATA() #get the data of the directory

print_to_json(format_dict(DATA), 'data_fat32.txt') #print the data in json format

