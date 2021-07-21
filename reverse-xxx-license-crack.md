> 某系统license生成工具，关键key信息已修改

```
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <errno.h>
#include <sys/socket.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <linux/netdevice.h>
#include <linux/types.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <unistd.h>
#include <cpuid.h>
#include <fcntl.h>
#include <scsi/sg.h>
#include <stdbool.h>
#include <time.h>
#include <openssl/md5.h>
#include <openssl/pem.h>
#include <openssl/bio.h>
#include <openssl/evp.h>
#include <openssl/err.h>

#pragma pack(1)
typedef struct cpu_info_{
    uint8_t cpuid[32];
    uint8_t brand[64];
    uint8_t processors[4];
}cpu_info;
typedef struct machine_info_{
    uint8_t eth0_mac[6];
    uint8_t em1_mac[6];
    cpu_info cpu;
    uint8_t serial[32];
    uint8_t reserved[111];
}machine_info;
#pragma apop()

#define SG_CHECK_CONDITION    0x02
#define SG_DRIVER_SENSE        0x08

#define SG_ATA_16        0x85
#define SG_ATA_16_LEN        16

#define SG_ATA_LBA48        1
#define SG_ATA_PROTO_NON_DATA    ( 3 << 1)
#define SG_ATA_PROTO_PIO_IN    ( 4 << 1)
#define SG_ATA_PROTO_PIO_OUT    ( 5 << 1)
#define SG_ATA_PROTO_DMA    ( 6 << 1)
#define SG_ATA_PROTO_UDMA_IN    (11 << 1) /* not yet supported in libata */
#define SG_ATA_PROTO_UDMA_OUT    (12 << 1) /* not yet supported in libata */

#define ATA_USING_LBA        (1 << 6)

enum {
    ATA_OP_CHECKPOWERMODE1        = 0xe5,
    ATA_OP_CHECKPOWERMODE2        = 0x98,
    ATA_OP_DOORLOCK            = 0xde,
    ATA_OP_DOORUNLOCK        = 0xdf,
    ATA_OP_FLUSHCACHE        = 0xe7,
    ATA_OP_FLUSHCACHE_EXT        = 0xea,
    ATA_OP_IDENTIFY            = 0xec,
    ATA_OP_PIDENTIFY        = 0xa1,
    ATA_OP_SECURITY_DISABLE        = 0xf6,
    ATA_OP_SECURITY_ERASE_PREPARE    = 0xf3,
    ATA_OP_SECURITY_ERASE_UNIT    = 0xf4,
    ATA_OP_SECURITY_FREEZE_LOCK    = 0xf5,
    ATA_OP_SECURITY_SET_PASS    = 0xf1,
    ATA_OP_SECURITY_UNLOCK        = 0xf2,
    ATA_OP_SETFEATURES        = 0xef,
    ATA_OP_SETIDLE1            = 0xe3,
    ATA_OP_SETIDLE2            = 0x97,
    ATA_OP_SLEEPNOW1        = 0xe5,
    ATA_OP_SLEEPNOW2        = 0x99,
    ATA_OP_SMART            = 0xb0,
    ATA_OP_STANDBYNOW1        = 0xe0,
    ATA_OP_STANDBYNOW2        = 0x94,
};

enum {
    SG_CDB2_TLEN_NODATA    = 0 << 0,
    SG_CDB2_TLEN_FEAT    = 1 << 0,
    SG_CDB2_TLEN_NSECT    = 2 << 0,

    SG_CDB2_TLEN_BYTES    = 0 << 2,
    SG_CDB2_TLEN_SECTORS    = 1 << 2,

    SG_CDB2_TDIR_TO_DEV    = 0 << 3,
    SG_CDB2_TDIR_FROM_DEV    = 1 << 3,

    SG_CDB2_CHECK_COND    = 1 << 5,
};

static void dump_bytes (const char *prefix, unsigned char *p, int len)
{
    int i;

    if (prefix)
        fprintf(stderr, "%s: ", prefix);
    for (i = 0; i < len; ++i)
        fprintf(stderr, " %02x", p[i]);
    fprintf(stderr, "\n");
}


#define START_SERIAL 10 /* ASCII serial number */
#define LENGTH_SERIAL 10 /* 10 words (20 bytes or characters) */

int get_sata_serial(char *serial)
{
    int fd = 0;

    static __u8 args[512] = { 0 };
    __u16 *id = (void *)(args);

    void *data = (void *)(args);
    unsigned int data_bytes = 512;

    unsigned char cdb[SG_ATA_16_LEN] = { 0 };
    unsigned char sb[32], *desc;
    unsigned char ata_status, ata_error;
    struct sg_io_hdr io_hdr;


//打开设备

    fd = open("/dev/sda", O_RDONLY);
    if (fd < 0) {
        printf("open /dev/sda error, try sudo\n");
        return -1;
    }


//设置cmdp

    cdb[ 0] = SG_ATA_16;
    cdb[ 1] = SG_ATA_PROTO_PIO_IN;
    cdb[ 2] = SG_CDB2_CHECK_COND;
    cdb[2] |= SG_CDB2_TLEN_NSECT | SG_CDB2_TLEN_SECTORS;
    cdb[2] |= SG_CDB2_TDIR_FROM_DEV;
    cdb[13] = ATA_USING_LBA;
    cdb[14] = ATA_OP_IDENTIFY;

//设置sdp

    memset(&(sb[0]), 0, sizeof(sb));

//设置sg_io_hdr结构

    memset(&io_hdr, 0, sizeof(struct sg_io_hdr));
    io_hdr.interface_id    = 'S';
    io_hdr.cmd_len        = SG_ATA_16_LEN;
    io_hdr.mx_sb_len    = sizeof(sb);
    io_hdr.dxfer_direction    = SG_DXFER_FROM_DEV;
    io_hdr.dxfer_len    = data_bytes;
    io_hdr.dxferp        = data;
    io_hdr.cmdp        = cdb;
    io_hdr.sbp        = sb;
    io_hdr.timeout        = 10000; /* msecs */


//调用ioctl

    if (ioctl(fd, SG_IO, &io_hdr) == -1) {
        fprintf(stderr, "SG_IO ioctl not supported\n");
        return -1;    /* SG_IO not supported */
    }

//检查sg_io_hdr中的状态值

    if (io_hdr.host_status || io_hdr.driver_status != SG_DRIVER_SENSE
     || (io_hdr.status && io_hdr.status != SG_CHECK_CONDITION))
    {
         errno = EIO;
        return -2;
    }

//检查sdp中的状态值

    if (sb[0] != 0x72 || sb[7] < 14) {
        errno = EIO;
        return -3;
    }
    desc = sb + 8;
    if (desc[0] != 9 || desc[1] < 12){
        errno = EIO;
        return -4;
    }

    ata_error = desc[3];
    ata_status = desc[13];
    if (ata_status & 0x01) {    /* ERR_STAT */
        errno = EIO;
        return -5;
    }

    char buf[LENGTH_SERIAL*20] = {'\0'};
    memcpy(buf, &id[START_SERIAL], LENGTH_SERIAL*2);
    for(int i = 0; i < LENGTH_SERIAL*2; i += 2){
      serial[i] = buf[i + 1];
      serial[i + 1] = buf[i];
    }
    printf("Disk Serial Number: %s\n", serial);

    return 0;
}

static inline void cpuid(int code, uint32_t *a, uint32_t *d) {
    asm volatile("cpuid":"=a"(*a),"=d"(*d):"a"(code):"ecx","ebx");
}

static inline int cpuid_string(int code, uint32_t *where) {
    asm volatile("cpuid":"=a"(*where),"=b"(*(where+1)),
      "=c"(*(where+2)),"=d"(*(where+3)):"a"(code));
    return (int)where[0];
}

int get_brand(char *brand){
    char buf[48 + 1] = {'\0'};
    uint32_t cpu_code = 0x80000002;

    for(int i = 0; i <= 2; i++){
        cpuid_string(0x80000002 + i, (uint32_t *)&buf[16 * i]);
    }

    strcpy(brand, buf);
    sprintf(brand, "%ld", sysconf(_SC_NPROCESSORS_CONF));
    printf("get_brand: %s\n", brand);
    return 0;
}

int get_cpu_id(char *id){
    unsigned int level = 1;
    unsigned eax = 3 /* processor serial number */, ebx = 0, ecx = 0, edx = 0;
    __get_cpuid(level, &eax, &ebx, &ecx, &edx);

    // byte swap
    //int first = ((eax >> 24) & 0xff) | ((eax << 8) & 0xff0000) | ((eax >> 8) & 0xff00) | ((eax << 24) & 0xff000000);
    //int last = ((edx >> 24) & 0xff) | ((edx << 8) & 0xff0000) | ((edx >> 8) & 0xff00) | ((edx << 24) & 0xff000000);

    sprintf(id, "%08X%08X%08X%08X", edx, eax, 0, 0);
    printf("get_cpu_id: %s\n", id);
    return 0;
}

int get_mac_address(char *name, char *mac, int fmt_type){
    struct ifreq s;
    int fd = socket(PF_INET, SOCK_DGRAM, IPPROTO_IP);

    char *fmt = NULL;
    if(fmt_type == 1){
        fmt = "%02x%02x%02x%02x%02x%02x";
    }
    else{
        fmt = "%02x-%02x-%02x-%02x-%02x-%02x";
    }
    strcpy(s.ifr_name, name);
    if (0 == ioctl(fd, SIOCGIFHWADDR, &s)){
        sprintf(mac, fmt,
        (unsigned char) s.ifr_addr.sa_data[0],
        (unsigned char) s.ifr_addr.sa_data[1],
        (unsigned char) s.ifr_addr.sa_data[2],
        (unsigned char) s.ifr_addr.sa_data[3],
        (unsigned char) s.ifr_addr.sa_data[4],
        (unsigned char) s.ifr_addr.sa_data[5]);
    }
    close(fd);

    return 0;
}

machine_info *get_machine_info(){
    machine_info *info = (machine_info *)malloc(sizeof(machine_info));
    memset((void *)info, 0, sizeof(machine_info));
    get_mac_address("eth0", info->eth0_mac, 0);
    get_mac_address("em1", info->em1_mac, 0);
    get_cpu_id(info->cpu.cpuid);
    get_brand(info->cpu.brand);
    get_sata_serial(info->serial);
    return info;
}

// initial permutation IP
const static char IP_Table[64] = {
	58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4,
	62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8,
	57, 49, 41, 33, 25, 17,  9, 1, 59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7
};
// final permutation IP^-1
const static char IPR_Table[64] = {
	40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31,
	38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27,
	34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41,  9, 49, 17, 57, 25
};
// expansion operation matrix
static const char E_Table[48] = {
	32,  1,  2,  3,  4,  5,  4,  5,  6,  7,  8,  9,
	 8,  9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17,
	16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25,
	24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32,  1
};
// 32-bit permutation function P used on the output of the S-boxes
const static char P_Table[32] = {
	16, 7, 20, 21, 29, 12, 28, 17, 1,  15, 23, 26, 5,  18, 31, 10,
	2,  8, 24, 14, 32, 27, 3,  9,  19, 13, 30, 6,  22, 11, 4,  25
};
// permuted choice table (key)
const static char PC1_Table[56] = {
	57, 49, 41, 33, 25, 17,  9,  1, 58, 50, 42, 34, 26, 18,
	10,  2, 59, 51, 43, 35, 27, 19, 11,  3, 60, 52, 44, 36,
	63, 55, 47, 39, 31, 23, 15,  7, 62, 54, 46, 38, 30, 22,
	14,  6, 61, 53, 45, 37, 29, 21, 13,  5, 28, 20, 12,  4
};
// permuted choice key (table)
const static char PC2_Table[48] = {
	14, 17, 11, 24,  1,  5,  3, 28, 15,  6, 21, 10,
	23, 19, 12,  4, 26,  8, 16,  7, 27, 20, 13,  2,
	41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48,
	44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32
};
// number left rotations of pc1
const static char LOOP_Table[16] = {
	1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1
};
// The (in)famous S-boxes
const static char S_Box[8][4][16] = {
	// S1
	14,	 4,	13,	 1,  2, 15, 11,  8,  3, 10,  6, 12,  5,  9,  0,  7,
	 0, 15,  7,  4, 14,  2, 13,  1, 10,  6, 12, 11,  9,  5,  3,  8,
	 4,  1, 14,  8, 13,  6,  2, 11, 15, 12,  9,  7,  3, 10,  5,  0,
    15, 12,  8,  2,  4,  9,  1,  7,  5, 11,  3, 14, 10,  0,  6, 13,
	// S2
    15,  1,  8, 14,  6, 11,  3,  4,  9,  7,  2, 13, 12,  0,  5, 10,
	 3, 13,  4,  7, 15,  2,  8, 14, 12,  0,  1, 10,  6,  9, 11,  5,
	 0, 14,  7, 11, 10,  4, 13,  1,  5,  8, 12,  6,  9,  3,  2, 15,
    13,  8, 10,  1,  3, 15,  4,  2, 11,  6,  7, 12,  0,  5, 14,  9,
	// S3
    10,  0,  9, 14,  6,  3, 15,  5,  1, 13, 12,  7, 11,  4,  2,  8,
	13,  7,  0,  9,  3,  4,  6, 10,  2,  8,  5, 14, 12, 11, 15,  1,
	13,  6,  4,  9,  8, 15,  3,  0, 11,  1,  2, 12,  5, 10, 14,  7,
     1, 10, 13,  0,  6,  9,  8,  7,  4, 15, 14,  3, 11,  5,  2, 12,
	// S4
     7, 13, 14,  3,  0,  6,  9, 10,  1,  2,  8,  5, 11, 12,  4, 15,
	13,  8, 11,  5,  6, 15,  0,  3,  4,  7,  2, 12,  1, 10, 14,  9,
	10,  6,  9,  0, 12, 11,  7, 13, 15,  1,  3, 14,  5,  2,  8,  4,
     3, 15,  0,  6, 10,  1, 13,  8,  9,  4,  5, 11, 12,  7,  2, 14,
	// S5
     2, 12,  4,  1,  7, 10, 11,  6,  8,  5,  3, 15, 13,  0, 14,  9,
	14, 11,  2, 12,  4,  7, 13,  1,  5,  0, 15, 10,  3,  9,  8,  6,
	 4,  2,  1, 11, 10, 13,  7,  8, 15,  9, 12,  5,  6,  3,  0, 14,
    11,  8, 12,  7,  1, 14,  2, 13,  6, 15,  0,  9, 10,  4,  5,  3,
	// S6
    12,  1, 10, 15,  9,  2,  6,  8,  0, 13,  3,  4, 14,  7,  5, 11,
	10, 15,  4,  2,  7, 12,  9,  5,  6,  1, 13, 14,  0, 11,  3,  8,
	 9, 14, 15,  5,  2,  8, 12,  3,  7,  0,  4, 10,  1, 13, 11,  6,
     4,  3,  2, 12,  9,  5, 15, 10, 11, 14,  1,  7,  6,  0,  8, 13,
	// S7
     4, 11,  2, 14, 15,  0,  8, 13,  3, 12,  9,  7,  5, 10,  6,  1,
	13,  0, 11,  7,  4,  9,  1, 10, 14,  3,  5, 12,  2, 15,  8,  6,
	 1,  4, 11, 13, 12,  3,  7, 14, 10, 15,  6,  8,  0,  5,  9,  2,
     6, 11, 13,  8,  1,  4, 10,  7,  9,  5,  0, 15, 14,  2,  3, 12,
	// S8
    13,  2,  8,  4,  6, 15, 11,  1, 10,  9,  3, 14,  5,  0, 12,  7,
	 1, 15, 13,  8, 10,  3,  7,  4, 12,  5,  6, 11,  0, 14,  9,  2,
	 7, 11,  4,  1,  9, 12, 14,  2,  0,  6, 10, 13, 15,  3,  5,  8,
     2,  1, 14,  7,  4, 10,  8, 13, 15, 12,  9,  0,  3,  5,  6, 11
};

//////////////////////////////////////////////////////////////////////////

typedef bool    (*PSubKey)[16][48];

//////////////////////////////////////////////////////////////////////////

static void DES(char Out[8], char In[8], const PSubKey pSubKey, bool Type);//标准DES加/解密
static void SetKey(const char* Key, int len);// 设置密钥
static void SetSubKey(PSubKey pSubKey, const char Key[8]);// 设置子密钥
static void F_func(bool In[32], const bool Ki[48]);// f 函数
static void S_func(bool Out[32], const bool In[48]);// S 盒代替
static void Transform(bool *Out, bool *In, const char *Table, int len);// 变换
static void Xor(bool *InA, const bool *InB, int len);// 异或
static void RotateL(bool *In, int len, int loop);// 循环左移
static void ByteToBit(bool *Out, const char *In, int bits);// 字节组转换成位组
static void BitToByte(char *Out, const bool *In, int bits);// 位组转换成字节组

//////////////////////////////////////////////////////////////////////////

static bool SubKey[2][16][48];// 16圈子密钥
static bool Is3DES;// 3次DES标志
static char Tmp[256], deskey[16];

//////////////////////////////////////////////////////////////////////////

//////////////////////////////////////////////////////////////////////////
// Code starts from Line 130
//////////////////////////////////////////////////////////////////////////
bool Des_Go(char *Out, char *In, long datalen, const char *Key, int keylen, bool Type)
{
    if( !( Out && In && Key && (datalen=(datalen+7)&0xfffffff8) ) )
		return false;
	SetKey(Key, keylen);
	if( !Is3DES ) {   // 1次DES
		for(long i=0,j=datalen>>3; i<j; ++i,Out+=8,In+=8)
			DES(Out, In, &SubKey[0], Type);
	} else{   // 3次DES 加密:加(key0)-解(key1)-加(key0) 解密::解(key0)-加(key1)-解(key0)
		for(long i=0,j=datalen>>3; i<j; ++i,Out+=8,In+=8) {
			DES(Out, In,  &SubKey[0], Type);
			DES(Out, Out, &SubKey[1], !Type);
			DES(Out, Out, &SubKey[0], Type);
		}
	}
	return true;
}
void SetKey(const char* Key, int len)
{
	memset(deskey, 0, 16);
	memcpy(deskey, Key, len>16?16:len);
	//SetSubKey(&SubKey[0], &deskey[0]);
	SetSubKey(&SubKey[1], &deskey[8]);
	Is3DES = len>8 ? (SetSubKey(&SubKey[1], &deskey[8]), true) : false;
}
void DES(char Out[8], char In[8], const PSubKey pSubKey, bool Type)
{
    static bool M[64], tmp[32], *Li=&M[0], *Ri=&M[32];
    ByteToBit(M, In, 64);
    Transform(M, M, IP_Table, 64);
    if( Type == 0 ){
        for(int i=0; i<16; ++i) {
            memcpy(tmp, Ri, 32);
            F_func(Ri, (*pSubKey)[i]);
            Xor(Ri, Li, 32);
            memcpy(Li, tmp, 32);
        }
    }else{
        for(int i=15; i>=0; --i) {
            memcpy(tmp, Li, 32);
            F_func(Li, (*pSubKey)[i]);
            Xor(Li, Ri, 32);
            memcpy(Ri, tmp, 32);
        }
	}
    Transform(M, M, IPR_Table, 64);
    BitToByte(Out, M, 64);
}
void SetSubKey(PSubKey pSubKey, const char Key[8])
{
    static bool K[64], *KL=&K[0], *KR=&K[28];
    ByteToBit(K, Key, 64);
    Transform(K, K, PC1_Table, 56);
    for(int i=0; i<16; ++i) {
        RotateL(KL, 28, LOOP_Table[i]);
        RotateL(KR, 28, LOOP_Table[i]);
        Transform((*pSubKey)[i], K, PC2_Table, 48);
    }
}
void F_func(bool In[32], const bool Ki[48])
{
    static bool MR[48];
    Transform(MR, In, E_Table, 48);
    Xor(MR, Ki, 48);
    S_func(In, MR);
    Transform(In, In, P_Table, 32);
}
void S_func(bool Out[32], const bool In[48])
{
    for(char i=0,j,k; i<8; ++i,In+=6,Out+=4) {
        j = (In[0]<<1) + In[5];
        k = (In[1]<<3) + (In[2]<<2) + (In[3]<<1) + In[4];
		ByteToBit(Out, &S_Box[i][j][k], 4);
    }
}
void Transform(bool *Out, bool *In, const char *Table, int len)
{
    for(int i=0; i<len; ++i)
        Tmp[i] = In[ Table[i]-1 ];
    memcpy(Out, Tmp, len);
}
void Xor(bool *InA, const bool *InB, int len)
{
    for(int i=0; i<len; ++i)
        InA[i] ^= InB[i];
}
void RotateL(bool *In, int len, int loop)
{
    memcpy(Tmp, In, loop);
    memcpy(In, In+loop, len-loop);
    memcpy(In+len-loop, Tmp, loop);
}
void ByteToBit(bool *Out, const char *In, int bits)
{
    for(int i=0; i<bits; ++i)
        Out[i] = (In[i>>3]>>(i&7)) & 1;
}
void BitToByte(char *Out, const bool *In, int bits)
{
    memset(Out, 0, bits>>3);
    for(int i=0; i<bits; ++i)
        Out[i>>3] |= In[i]<<(i&7);
}

int Des_Make(char *out, char *in, int datalen, char *key, int keylen, int type){
    int rst = 0;
    if(datalen & 7){
        return rst;
    }
    for(int i = 0; i < datalen / 8; ++i){
        rst = Des_Go(out + 8 * i, in + 8 * i, 8, key, keylen, type);
        if(!rst) break;
    }
    return rst;
}

char *print_md5(unsigned char *md5){
    char buf[33] = {'\0'};
	for(int i = 0; i < 16; i++){
		sprintf(buf + 2*i, "%02X", md5[i]);
	}
	printf("%s\n",buf);
}

int md5(char *data, int datalen, unsigned char *buf){
	
	MD5_CTX ctx;
	MD5_Init(&ctx);
	MD5_Update(&ctx, data, datalen);
	MD5_Final(buf, &ctx);

	return 0;
}

int base64_encode(char *in_str, int in_len, char *out_str)
{
    BIO *b64, *bio;
    BUF_MEM *bptr = NULL;
    size_t size = 0;

    if (in_str == NULL || out_str == NULL)
        return -1;

    b64 = BIO_new(BIO_f_base64());
    bio = BIO_new(BIO_s_mem());
    bio = BIO_push(b64, bio);

    BIO_write(bio, in_str, in_len);
    BIO_flush(bio);

    BIO_get_mem_ptr(bio, &bptr);
    memcpy(out_str, bptr->data, bptr->length);
    out_str[bptr->length] = '\0';
    size = bptr->length;

    BIO_free_all(bio);
    return size;
}

int base64_decode(char *in_str, int in_len, char *out_str)
{
    BIO *b64, *bio;
    BUF_MEM *bptr = NULL;
    int counts;
    int size = 0;

    if (in_str == NULL || out_str == NULL)
        return -1;

    b64 = BIO_new(BIO_f_base64());
    BIO_set_flags(b64, BIO_FLAGS_BASE64_NO_NL);

    bio = BIO_new_mem_buf(in_str, in_len);
    bio = BIO_push(b64, bio);

    size = BIO_read(bio, out_str, in_len);
    out_str[size] = '\0';

    BIO_free_all(bio);
    return size;
}


int get_machine_code(char *info){
    char *key = "GetMemInfo";
    unsigned char md5_buf[16] = {'\0'};
    md5(key, strlen(key), md5_buf);
    char mac[32] = {'\0'};
    get_mac_address("enp3s0", mac, 1);
    //print_md5(md5_buf);
    unsigned char info_raw[32] = {'\0'};
    Des_Go(info_raw, mac, sizeof(info_raw), md5_buf, sizeof(md5_buf), 0);
    base64_encode(info_raw, sizeof(info_raw), info);
    return 0;
}

char *get_machine_code(){
    char *key = "xxx_secret_license";
    char *info = (char *)get_machine_info();
    char *out = (char *)malloc(256);
    memset(out, '\0', 256);
    Des_Make(out, info, 256, key, strlen(key), 0);
    return out;
}

int write_machine_info_file(char *filename){
    char *code = NULL;
    code = get_machine_code();
    if(code == NULL){
        printf("get machine code failed\n");
        return 0;
    }
    else{
        FILE *fd = NULL;
        fd = fopen(filename, "wb+");
        if(fd == NULL){
            printf("fopen %s failed\n", filename);
            return 0;
        }
        fwrite(code, 1, 256, fd);
        fclose(fd);
        return 1;
    }
}

int checkdate(char *date){
    char buf[32] = {'\0'};
    char *ptr = date;
    int year = 0, month = 0, day = 0, duration = 0, linenum = 0;
    memcpy(buf, date, 4);
    year = atoi(buf);
    ptr += 4;

    memset(buf, '\0', sizeof(buf));
    memcpy(buf, ptr, 2);
    month = atoi(buf);
    ptr += 2;

    memset(buf, '\0', sizeof(buf));
    memcpy(buf, ptr, 2);
    day = atoi(buf);
    ptr += 2;

    memset(buf, '\0', sizeof(buf));
    memcpy(buf, ptr, 4);
    duration = atoi(buf);
    ptr += 4;

    memset(buf, '\0', sizeof(buf));
    memcpy(buf, ptr, 4);
    linenum = atoi(buf);

    printf("destYear:%04d,destMonth:%02d,destDay:%02d,destDur:%02d,lineNum:%02d\n",
            year, month, day, duration, linenum);

    return 0;
}

int checkmachine(char *license){
    char *code = get_machine_code();
    for(int i = 0; i <= 239; ++i){
        if(license[i] != code[i]){
            return -1;
        }
    }
    return 0;
}

int checkone(char *code, char *data){
    char *key = "xxx_secret_license";
    char out[256] = {'\0'};
    int rst = 0;
    rst = Des_Make(out, data, 256, key, strlen(key), 1);
    if(rst == 0){
        printf("decode license code1 failed\n");
        return -1;
    }
    char license[256] = {'\0'};
    rst = Des_Make(license, out, 256, code, strlen(code), 1);
    if(rst == 0){
        printf("decode license code2 failed\n");
        return -1;
    }
    printf("machine code is:\n");
    //printf("%s\n", license);

    rst = 0;
    rst = checkmachine(license);
    if(rst != 0){
        printf("machine code not matched!\n");
        //return -1;
    }
    rst = 0;
    rst = checkdate(&license[0xF0]);
    if(rst != 0){
        printf("date expired\n");
        return -1;
    }
}

int checklicense(char *filename, char *code){
    FILE *fp = NULL;
    fp = fopen(filename, "rb");
    if(fp == NULL){
        printf("cann't open license: %s\n", filename);
    }
    int flen = 0;
    char buf[256] = {'\0'};
    flen = fread(buf, 1, 256, fp);
    fclose(fp);
    if(flen != 256){
        printf("licese file: %s error\n", filename);
    }
    int rst = 0;
    rst = checkone(code, buf);
    printf("checkone: %d\n", rst);
}

int getinfo(char *filename) {
    int err = write_machine_info_file(filename);
    return 0;
}

int authorize(char *filename, char *code, char *duration, char *sessions, char *path){
    FILE *fp = NULL;
    fp = fopen(filename, "rb");
    if(fp == NULL){
        printf("cann't open machine code file: %s\n", filename);
        return -1;
    }
    int flen = 0;
    char buf[256] = {'\0'};
    flen = fread(buf, 1, 256, fp);
    fclose(fp);
    if(flen != 256){
        printf("machine code file: %s error\n", filename);
        return -1;
    }

    char date[16 + 1] = {'\0'};
    time_t now;
    struct tm *timenow;
    time(&now);
    timenow = localtime(&now);
    //timenow->tm_year += atoi(duration)/12;
    //timenow->tm_mon += atoi(duration)%12;
    sprintf(date, "%04d%02d%02d", timenow->tm_year + 1900, timenow->tm_mon + 1, timenow->tm_mday);
    char dur[4] = {'\0'};
    sprintf(dur, "%04d", atoi(duration));
    strcat(date, dur);
    strcat(date, sessions);
    memcpy(&buf[0xF0], date, 16);

    char *key = "xxx_secret_license";
    char out[256] = {'\0'};
    int rst = 0;
    rst = Des_Make(out, buf, 256, code, strlen(code), 0);
    if(rst == 0){
        printf("encode license code1 failed\n");
        return -1;
    }
    char license[256] = {'\0'};
    rst = 0;
    rst = Des_Make(license, out, 256, key, strlen(key), 0);
    if(rst == 0){
        printf("encode license code2 failed\n");
        return -1;
    }

    fp = NULL;
    fp = fopen(path, "wb+");
    if(fp == NULL){
        printf("cann't open license file: %s\n", path);
        return -1;
    }
    fwrite(license, 1, 256, fp);
    fclose(fp);

    return 0;
}

//int main(int argc, char *argv[]) {
//    if(argc < 2){
//        printf("functions: getinfo, checklicense, authorize\n");
//        exit(-1);
//    }
//    if(strcmp(argv[1], "getinfo") == 0){
//        if(argc != 3){
//            printf("getinfo path\n");
//            exit(-1);
//        }
//        getinfo(argv[2]);
//    }
//    if(strcmp(argv[1], "checklicense") == 0){
//        if(argc != 4){
//            printf("checklicense path code\n");
//            exit(-1);
//        }
//        checklicense(argv[2], argv[3]);
//    }
//    if(strcmp(argv[1], "authorize") == 0){
//        if(argc != 7){
//            printf("authorize machinepath code duration sessions licensepath\n");
//            exit(-1);
//        }
//        authorize(argv[2], argv[3], argv[4], argv[5], argv[6]);
//    }
//}

int getinfo(char *path) {
    char buf[64] = {0};
    get_machine_code(buf);
    FILE *fp = NULL;
    fp = fopen(path, "w");
    fwrite(buf, 1, strlen(buf), fp);
    fclose(fp);
    printf("%s\n", buf);
}

RSA *read_public_pem(const char *path){
    OPENSSL_add_all_algorithms_noconf();
    BIO *bio = BIO_new_file(path, "rb");
    BIO_set_flags(bio, 256);
    RSA *rsa = PEM_read_bio_RSApublicey(bio, 0, 0, 0);
    if(rsa == NULL){
        printf("read rsa public key failed\n");
    }
    return rsa;
}

RSA *read_private_pem(const char *path){
    OPENSSL_add_all_algorithms_noconf();
    BIO *bio = BIO_new_file(path, "rb");
    BIO_set_flags(bio, 256);
    RSA *rsa = PEM_read_bio_RSAPrivateKey(bio, 0, 0, 0);
    if(rsa == NULL){
        printf("read rsa private key failed\n");
    }
    return rsa;
}

int decrypt(RSA *rsa, char *src, int src_len, char **out_str, int *out_len) {

    int keylen = RSA_size(rsa);

    int rsa_padding = 0;
    int oncelen = keylen;
    if(*(int *)src == 0x44504f4e){
        //DPON
        rsa_padding = 3;
    }
    else if(*(int *)src == 0x53434b50){
        rsa_padding = 1;
        oncelen -= 11;
    }

    int plain_len = *((int *)src + 1);
    src_len -= 8;
    src += 8;

    memmove(src + 7, src + 8, src_len - 8);

    int times = (src_len - 1) / keylen;
    int delen = times * oncelen;
    char *de_data = (char *)malloc(delen);
    memset(de_data, 0, delen);
    *out_str = de_data;

    int rst = -1;
    for(int i = 0; i < times; i++){
        rst = RSA_public_decrypt(keylen, src + i * keylen, de_data + i * oncelen, rsa, rsa_padding);
        if(rst < 0){
            int err = ERR_get_error();
            printf("RSA public decrypt failed[%d]!\n", err);
            printf("%s\n", ERR_error_string(err, NULL));
            break;
        }
    }

    *out_len = plain_len;
}

const unsigned char license_server_public_key[140] = {
    0x30, 0x81, 0x89, 0x02, 0x81, 0x81, 0x00, 0xDA, 0xDE, 0xFA,
    0x9A, 0xF6, 0xE2, 0xB6, 0x8E, 0x60, 0x8A, 0x84, 0xAF, 0x6E,
    0x22, 0xD1, 0xDC, 0x2F, 0x24, 0x18, 0x7D, 0x5C, 0xF6, 0x76,
    0x62, 0x7F, 0x41, 0x10, 0xFF, 0x56, 0xBA, 0x16, 0xF2, 0x61,
    0x4C, 0xBA, 0x1C, 0x6F, 0xD0, 0xBE, 0x11, 0x9F, 0xDE, 0x70,
    0x56, 0x60, 0x4C, 0x6B, 0xD2, 0x64, 0xAF, 0xF2, 0x18, 0x51,
    0xDD, 0xF0, 0x11, 0xCB, 0x05, 0x82, 0x52, 0x41, 0x2D, 0x81,
    0x73, 0x39, 0xCA, 0xA7, 0x54, 0x2D, 0xE7, 0xF3, 0xF5, 0xDE,
    0xA2, 0x8E, 0x7D, 0xFC, 0x0B, 0x63, 0x44, 0x58, 0xE1, 0xC9,
    0xB7, 0x53, 0x76, 0xBB, 0x72, 0x42, 0x88, 0xCF, 0x2E, 0xD0,
    0xA9, 0x22, 0xFB, 0xD7, 0x03, 0xCF, 0xC4, 0x21, 0x0A, 0x57,
    0x45, 0x1E, 0x02, 0x75, 0x18, 0x5F, 0x8C, 0xD8, 0x84, 0x88,
    0x45, 0x1B, 0x22, 0x6B, 0x75, 0x19, 0xD6, 0x4D, 0x5E, 0x4E,
    0xC6, 0xE9, 0x3D, 0x74, 0xBB, 0x02, 0x03, 0x01, 0x00, 0x01
};
const unsigned  char license_server_public_key_fake[140] = {
    0x30, 0x81, 0x89, 0x02, 0x81, 0x81, 0x00, 0xCC, 0xD3, 0x74,
    0xEF, 0xFB, 0xA1, 0x00, 0xCA, 0xEE, 0x40, 0xF4, 0xC7, 0x78,
    0x07, 0xA7, 0xC5, 0xC3, 0xE1, 0x7B, 0x79, 0x8E, 0xEC, 0x7F,
    0xE6, 0x4B, 0xBF, 0xC2, 0x32, 0xF4, 0xF0, 0xFE, 0x39, 0xA5,
    0x73, 0x68, 0xDE, 0xDE, 0x8F, 0xA4, 0xE7, 0x31, 0x6B, 0x2E,
    0xF7, 0x47, 0x4C, 0x82, 0x38, 0xB4, 0x7F, 0x6E, 0x36, 0x2C,
    0x12, 0xB8, 0xA2, 0x7A, 0x7A, 0x56, 0x3B, 0xBB, 0x03, 0xF4,
    0x42, 0x75, 0xB5, 0x03, 0x26, 0xFE, 0x8C, 0x6B, 0x02, 0x32,
    0x35, 0x52, 0xEC, 0x76, 0x7E, 0xEB, 0x67, 0xF9, 0xE1, 0xBC,
    0xE5, 0xE8, 0x44, 0xDF, 0x7B, 0x4D, 0x68, 0xE0, 0xC7, 0xFC,
    0xC5, 0x0B, 0xD5, 0xE2, 0x4C, 0xAA, 0xFB, 0x60, 0x45, 0x56,
    0xCB, 0xFB, 0xFF, 0xFA, 0x46, 0x42, 0xD7, 0xCB, 0xF3, 0xC3,
    0x59, 0x8D, 0x5A, 0x87, 0x1E, 0x0B, 0xC9, 0x91, 0xA5, 0xD9,
    0x85, 0xE2, 0xAC, 0xEA, 0x1F, 0x02, 0x03, 0x01, 0x00, 0x01
};

RSA *SimpleRSA_Readpublicey(const unsigned char *data, int len){
    if(len != 140){
        return NULL;
    }
    RSA *rsa = RSA_new();
    if(rsa == NULL){
        return NULL;
    }
    rsa->n = BN_bin2bn(data + 7, 128, 0);
    rsa->e = BN_bin2bn(data + 137, 3, 0);
}

int SimpleRSA_PublicDecryptBuffer(RSA *rsa, const char *src_buf, int src_len, char *result){

    int keylen = 128;
    int oncelen = 117;//128 - 11
    int times = (src_len - 4) / 128;
    int rsa_padding = 1;

    int rst = 0;
    for(int i = 0; i < times; i++){
        rst = RSA_public_decrypt(keylen, src_buf + i * keylen, result + i * oncelen, rsa, rsa_padding);
        if(rst < 0){
            int err = ERR_get_error();
            printf("RSA public decrypt failed[%d]!\n", err);
            printf("%s\n", ERR_error_string(err, NULL));
            break;
        }
    }

    return 1;
}

int verify_one_self_sig_file(RSA *rsa, const char *path){

    FILE *fp = NULL;
    fp = fopen(path, "r");
    fseek(fp, 0, 2);
    int en_len = ftell(fp);
    fseek(fp, 0, 0);
    char *en_data = (char *)malloc(en_len);
    fread(en_data, en_len, 1, fp);
    fclose(fp);

    char *sig_data = en_data + (en_len - 256);
    const char *version_str = "XXXSIGNv1";

    char *sig_en_data = sig_data + strlen(version_str) + 4;//4 bytes for int datalen
    char *out = (char *)malloc(128);
    memset(out, 0, 128);


    SimpleRSA_PublicDecryptBuffer(rsa, sig_en_data, 256 - strlen(version_str), out);

    unsigned char md5_digest[16] = {0};
    md5(en_data, en_len - 256, md5_digest);


    print_md5(md5_digest);
    print_md5(out);

    free(out);
}

//int verify_module_sign_common(RSA *rsa, void *sig, const char *lic_file, const char *server_module_path, bool *test_version){
//    int rst = -1;
//    if(sig != NULL){
//        //rst = verify_one_sig_file(rsa, sig, server_module_path);;
//    }
//    else{
//        rst = verify_one_self_sig_file(rsa, server_module_path);
//    }
//    if(rst != 2 && rst){
//        if(rst <= 4){
//            switch(rst){
//                case 3: return 4;
//                case 1: return 2;
//                case 4: return 5;
//                case 2: return 3;
//            }
//        }
//    }
//    return 0;
//}
//
//int verify_module_sign(const char *sig_file, const char *lic_file, const char *server_module_path, bool *test_version){
//    if(sig_file != NULL){
//        printf("not supported yet!\n");
//        return 0;
//    }
//    RSA *rsa = SimpleRSA_Readpublicey(license_server_public_key, sizeof(license_server_public_key));
//
//    verify_module_sign_common(rsa, sig, lic_file, server_module_path, test_version);
//}
//
//int verify_license(const char *lic_path, const char *sig_file){
//    //get module name from addr
//    const char *server_module_path = "";
//    verify_module_sign(sig_file, lic_file, server_module_path, &test_version);
//}

int show_license(char *public_pem, char *license_path, char *isfake) {

    int fake = atoi(isfake);

    RSA *rsa = read_public_pem(public_pem);

    FILE *fp = NULL;
    fp = fopen(license_path, "r");
    fseek(fp, 0, 2);
    int en_len = ftell(fp);
    fseek(fp, 0, 0);
    char *en_data = (char *)malloc(en_len);
    fread(en_data, en_len, 1, fp);
    fclose(fp);

    if(en_len > 256){
        //XXXSIGN info
        en_len -= 256;
    }

    char *out = NULL;
    int outlen = 0;
    decrypt(rsa, en_data, en_len, &out, &outlen);
    printf("%s\n", out);
    free(out);

    RSA *rsa2 = NULL;
    if(fake == 0){
        rsa2 = SimpleRSA_Readpublicey(license_server_public_key, sizeof(license_server_public_key));
    }
    else{
        rsa2 = rsa;
    }

    verify_one_self_sig_file(rsa2, license_path);
}

int encrypt(char *private_pem, char *license_info, char **out, int *outlen) {

    int rsa_padding = RSA_PKCS1_PADDING;
    RSA *rsa = read_private_pem(private_pem);
    
    int keylen = RSA_size(rsa);

    int oncelen = keylen;
    if(rsa_padding == 1){
        oncelen -= 11;
    }
    int times = (strlen(license_info) - 1) / oncelen + 1;
    int outbuflen = keylen * times;
    char *outbuf = (char *)malloc(outbuflen);
    memset(outbuf, 0, outbuflen);
    memcpy(outbuf, license_info, strlen(license_info));

    int rst = -1;
    for(int i = 0; i < times; i += 1){
        rst = RSA_private_encrypt(oncelen, license_info + i * oncelen, outbuf + i * keylen, rsa, rsa_padding);
        if(rst < 0){
            int err = ERR_get_error();
            printf("RSA private encrypt failed[%d]!\n", err);
            printf("%s\n", ERR_error_string(err, NULL));
        }
    }

    *out = outbuf;
    *outlen = outbuflen;
}

int authorize_license(char *info_path, char *private_key, char *license_path){

    FILE *fp = NULL;
    fp = fopen(info_path, "r");
    fseek(fp, 0, 2);
    int infolen = ftell(fp);
    fseek(fp, 0, 0);
    char *license_info = (char *)malloc(infolen);
    fread(license_info, infolen, 1, fp);
    fclose(fp);

    char *out = NULL;
    int outlen = 0;

    encrypt(private_key, license_info, &out, &outlen);

    int datalen = outlen + 9;
    char *data = (char *)malloc(datalen);

    int rsa_padding = 1;

    char *padding_text = NULL;
    if(rsa_padding == 3){
        padding_text = "NOPD";
    }
    else if(rsa_padding == 1){
        padding_text = "PKCS";
    }
    memcpy(data, padding_text, 4);
    *((int *)data + 1) = strlen(license_info);

    memcpy(data + 8, out, outlen);
    memmove(data + 8 + 8, data + 8 + 7, outlen);
    data[15] = 'I';

    char sign_data[256] = {0};
    char md5_digest[16] = {0};
    md5(data, datalen, md5_digest);

    const char *version_str = "XXXSIGNv1";
    memcpy(sign_data, version_str, strlen(version_str));
    *((int *)sign_data + 2) = 16;

    RSA *rsa = read_private_pem(private_key);
    int rst = RSA_private_encrypt(117, md5_digest, sign_data + 12, rsa, rsa_padding);
    if(rst < 0){
        int err = ERR_get_error();
        printf("RSA private encrypt failed[%d]!\n", err);
        printf("%s\n", ERR_error_string(err, NULL));
    }

    FILE *fp_save = fopen(license_path, "w");
    fwrite(data, 1, datalen, fp_save);
    fwrite(sign_data, 1, 256, fp_save);
    fclose(fp_save);
}

/* binary search in memory */
int memsearch(const char *hay, int haysize, const char *needle, int needlesize) {
    int haypos, needlepos;
    haysize -= needlesize;
    for (haypos = 0; haypos <= haysize; haypos++) {
        for (needlepos = 0; needlepos < needlesize; needlepos++) {
            if (hay[haypos + needlepos] != needle[needlepos]) {
                // Next character in haystack.
                break;
            }
        }
        if (needlepos == needlesize) {
            return haypos;
        }
    }
    return -1;
}

int build_fake_so(char *src, char *private_key, char *public_pem, char *dst, char *islicense){
    
    int license = atoi(islicense);

    RSA *rsa = read_public_pem(public_pem);

    FILE *fp = NULL;
    fp = fopen(src, "r");
    fseek(fp, 0, 2);
    int buflen = ftell(fp);
    fseek(fp, 0, 0);
    char *buf = (char *)malloc(buflen);
    fread(buf, buflen, 1, fp);
    fclose(fp);

    if(license != 0){
        unsigned char data[140] = {0};
        memcpy(data, license_server_public_key, 140);

        int bnrst = -1;
        bnrst = BN_bn2bin(rsa->n, data + 7);
        bnrst = BN_bn2bin(rsa->e, data + 137);

        int offset = memsearch(buf, buflen, license_server_public_key, 140);
        memcpy(buf + offset, data, 140);
        //char *test_str = "start to init soft license info...";
        //char *test_str2 = "START TO INIT SOFT LICENSE INFO...";
        //int offset2 = memsearch(buf, buflen, test_str, strlen(test_str));
        //memcpy(buf + offset2, test_str2, strlen(test_str));
    }

    int rsa_padding = 1;
    
    char sign_data[256] = {0};
    char md5_digest[16] = {0};
    md5(buf, buflen - 256, md5_digest);

    const char *version_str = "XXXSIGNv1";
    memcpy(sign_data, version_str, strlen(version_str));
    *((int *)sign_data + 2) = 16;

    RSA *rsa2 = read_private_pem(private_key);
    int rst = RSA_private_encrypt(117, md5_digest, sign_data + 12, rsa2, rsa_padding);
    if(rst < 0){
        int err = ERR_get_error();
        printf("RSA private encrypt failed[%d]!\n", err);
        printf("%s\n", ERR_error_string(err, NULL));
    }

    FILE *fpdst = NULL;
    fpdst = fopen(dst, "w");
    fwrite(buf, 1, buflen - 256, fpdst);
    fwrite(sign_data, 1, 256, fpdst);
    fclose(fpdst);
}

int main(int argc, char *argv[]) {
    if(argc < 2){
        printf("functions:\n\tget\tget machine info code\n\tshow\tshow license info\n\tauth\tauthorize to license info\n\tverify\tverify a self signed file with default rsa\n\tfake\tbuild fake so\n");
        exit(-1);
    }
    if(strcmp(argv[1], "get") == 0){
        if(argc != 3){
            printf("get path/to/save\n");
            exit(-1);
        }
        getinfo(argv[2]);
    }
    if(strcmp(argv[1], "show") == 0){
        if(argc != 5){
            printf("show path/to/public/key path/to/license isfake\n");
            exit(-1);
        }
        show_license(argv[2], argv[3], argv[4]);
    }
    if(strcmp(argv[1], "verify") == 0){
        if(argc != 4){
            printf("verify path/to/self/signed/file default\n");
            exit(-1);
        }
        RSA *rsa = NULL;
        if(strcmp(argv[3], "default") == 0){
            rsa = SimpleRSA_Readpublicey(license_server_public_key, sizeof(license_server_public_key));
        }
        else{
            //rsa = read_public_pem(argv[3]);
            rsa = SimpleRSA_Readpublicey(license_server_public_key_fake, sizeof(license_server_public_key));
        }
        verify_one_self_sig_file(rsa, argv[2]);
        
    }
    if(strcmp(argv[1], "auth") == 0){
        if(argc != 5){
            printf("auth path/of/auth/info path/to/private/key path/to/save/license\n");
            exit(-1);
        }
        authorize_license(argv[2], argv[3], argv[4]);
    }
    if(strcmp(argv[1], "fake") == 0){
        if(argc != 7){
            printf("fake path/to/original/so path/to/private/key path/to/public/key path/to/fake/so islicense\n");
            exit(-1);
        }
        build_fake_so(argv[2], argv[3], argv[4], argv[5], argv[6]);
    }
}
```
