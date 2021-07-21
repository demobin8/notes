> 原样的笔记，估计大部分人看了也不知道这是啥，不改了都放出来。。。

tracker分析
请求tracker server ip
--------------------无用---------------------------
```
typedef struct _TrackerServerReq
{
    uint32_t checksum;\x63\x\xd8\x60\x93
    uint32_t un2;//\x14\x02\x00\x00
    uint16_t un3;//\x00\x01
    uint16_t delim;//\x0c\x01
    uint16_t pad;
    uint8_t  vid[16];
}TrackerReq;

typedef struct _PeerInfo
{
    uint16_t delim;//\x0c\x00
    uint32_t ip;//\x58\x01\xa8\xc0
    uint16_t port;//\x3b\xc9
    uint8_t  operator;//\x01
}PeerInfo;

typedef struct _TrackerServerRsp
{
    uint32_t checksum;
    uint32_t un2;
    uint8_t  pad[3];
    uint16_t cnt;
    PeerInfo peerinfo[rsp.cnt];
}TrackerRsp;
```
----------------------tracker部分------------------------------
tracker
client端口5041，tracker server的端口不确定，是从上面的请求中得到的。
```
typedef struct _TrackerReq
{
    uint32_t checksum;\\getpptvchecksum(uint8_t *data, int len)
    uint8_t  cmd;//\x31
    uint8_t  un20;//=req.un20
    uint16_t un21;//=req.un21
    uint16_t un3;//\x00\x01
    uint16_t delim;//\x0c\x01
    uint16_t pad;
    uint8_t  vid[16];
    uint8_t  id[16];
    uint16_t cnt;//\x32
    uint8_t  un4;//\xff
}TrackerReq;

typedef struct _PeerInfo
{
    uint32_t lanip;//\x58\x01\xa8\xc0
    uint16_t lanport;//\x3b\xc9
    uint16_t delim;//\x0c\x01
    uint32_t wanip;//\x58\x01\xa8\xc0
    uint16_t wanport;//\x3b\xc9
    uint32_t un1;
    uint32_t un2;
    uint16_t un3;
}PeerInfo;

typedef struct _TrackerRsp
{
    uint32_t checksum;\\getpptvchecksum(uint8_t *data, int len)
    uint8_t  cmd;//\x31
    uint8_t  un20;//=req.un20
    uint16_t un21;//=req.un21
    uint8_t  pad[3];
    uint8_t  vid[16];//=req.vid
    uint16_t cnt;
    PeerInfo peerinfo[rsp.cnt];
}TrackerRsp;
```
-----------------------------------------------------
peer分析
```
typedef struct _PeerHSReq
{
    uint32_t checksum;
    uint8_t  cmd;
    uint8_t  un20;
    uint16_t un21;
    uint8_t  pad;
    uint16_t delim;
    uint16_t un22;
    uint8_t  vid[16];
    uint8_t  id[16];
    uint32_t un3;
    uint16_t delim;
    uint16_t pad;
    PeerInfo peerinfo;//最后一个字节置0
    uint8_t  un[16];
}PeerHSReq;

typedef struct _PeerHSRsp
{
    uint32_t checksum;
    uint8_t  cmd;//\x52
    uint8_t  un20;//=req.un20
    uint16_t un21;//=req.un21
    uint8_t  pad;
    uint16_t delim;//\x0c\x01
    uint16_t un22;
    uint8_t  vid[16];
    uint8_t  id[16];
    uint32_t un3;
    uint16_t delim;
    uint16_t pad;
    PeerInfo peerinfo;//最后一个字节置0
    uint8_t  un[16];
}PeerHSRsp;

typedef struct _PeerDataReq
{
    uint32_t checksum;
    uint8_t  cmd;
    uint8_t  un20;
    uint16_t un21;//=req.un21
    uint8_t  pad;
    uint16_t delim;
    uint16_t un3;
    uint8_t  id[16];
    uint8_t  cnt;
    uint32_t index[req.cnt];
    uint8_t  un4[3];//\x00\x64\x00
}PeerDataReq;

typedef struct _PeerDataRsp
{
    uint32_t checksum;
    uint8_t  cmd;//\x52
    uint8_t  un20;//=req.un20
    uint16_t un21;//=req.un21
    uint8_t  pad;
    uint16_t delim;//
    uint16_t un3;
    uint8_t  id[16];
    uint8_t  id2[16];
    uint16_t offset;
    uint16_t index;
    uint16_t datalen;
}PeerDataRsp;
```
checksum算法python版
```
def getpptvchecksum(src, ishex):
    if ishex:
        srchex = src
    else:
        srchex = binascii.a2b_hex(src)
    print binascii.hexlify(srchex)
    length = len(srchex) - 4
    data = srchex[4:]
    cnt = length / 8
    #length -= 1
    index = 0
    csum = 0x10312312
    while cnt:
        h = struct.unpack_from("I", data, index)[0]
        index += 4
        l = struct.unpack_from("I", data, index)[0]
        csum ^= h ^ l ^ (csum>>6) ^ (csum<<14&0xffffffff)
        index += 4
        cnt -= 1
        length -= 8
    for i in range(length):
        b = struct.unpack_from("B", data, index + i)[0]
        csum ^= b ^ (csum<<7&0xffffffff) ^ (csum>>13)
    print "0x%x"%csum
```
checksum算法c版
```
unsigned int pptvchecksum(unsigned char *data, int len)
{
	int length = len - 4;
	data += 4;
	int cnt = length/8;
	int index = 0;
	unsigned int csum = 0x10312312;
	unsigned int h, l;
	while(cnt)
	{
		h = *(unsigned int*)(data + index);
		index += 4;
		l = *(unsigned int*)(data + index);
		csum ^= h ^ l ^ (csum >> 6) ^ (csum << 14);
		index += 4;
		cnt -= 1;
		length -= 8;
	}
	int i;
	for(i = 0; i < length; i++)
	{
		csum ^= *(data + index + i) ^ (csum << 7) ^ (csum >> 13);
	}
	return csum;
}
```
http下载分析

下载地址
参数key为必要项
http://61.131.55.82/0_fe5365301c0cdf208ffef8ac90d9fda0.mp4?key=587cbede66b23dbb9232eb481ec66dea&type=client&vvid=D0438D95-D4AA-4AC9-B59F-44EECD5F6EA4&k=e3d7fbebe8514adc58ea7d8e3843e63c-1bdb-1421923357&cltver=3.5.8.0054
http://61.131.55.76/0_fe5365301c0cdf208ffef8ac90d9fda0.mp4?key=0f19dae81ba130fb9232eb481ec66dea&type=client&vvid=A0E589A5-0B04-455C-9425-69803C528D07&k=b682316270d2528a2e2ff267bc96319e-ee52-1421924435&cltver=3.5.8.0054
http://61.131.55.86/0_fe5365301c0cdf208ffef8ac90d9fda0.mp4?key=ee33a45f005f317e9232eb481ec66dea&type=client&vvid=79B0609A-0467-4997-AC7D-B8A5A0848C82&k=3a39f5612affb26588c6501745c6ede8-e3d8-1421924413&cltver=3.5.8.0054
```
header
Host: 61.131.55.76

User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E)

Connection: close

referer: http://client-play.pplive.cn/
```
来自于
http://client-play.pptv.com/v3/chplay4-0-18721089.xml&param=type%3Dclient%26userType%3D0%26areaType%3D63%26dns%3D134744072%26vvid%3D79B0609A%2D0467%2D4997%2DAC7D%2DB8A5A0848C82%26gslbversion%3D2%26k%5Fver%3D2%2E5%2E0%2E8544%26h265%3D2&zone=8&version=5&ppi=312c3633
参数可不要，header如下，必要项为Referer
```
Accept: */*

Referer: http://client-play.pplive.cn/

Accept-Encoding: gzip, deflate

User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E)

Host: client-play.pptv.com

Connection: Keep-Alive

Cache-Control: no-cache
```
st标签
时间
file标签
ft=0，1，2分别表示不同分辨率，filesize为各分辨率的文件大小
drag标签
no为分段序号，hl为headerlength即文件头的长度，fs为filesize即文件大小，of为offset即文件偏移

分析得到上述链接中key的算法为
对当前时间、pass(为"qqqqqww")进行TEA加密
pass: 
验证

key算法破解python版
```
def getpptvkey(date):
    
    keys = 'qqqqqww'
    key1tmp = (ctypes.c_uint8 *4)()
    for i, k in enumerate(keys):
    	key1tmp[i%4] ^= ord(k)
    key1 = struct.unpack('I', key1tmp)[0]
    key2 = ctypes.c_uint32((key1 >> 24) | (key1 << 8 )).value
    key3 = ctypes.c_uint32((key1 >> 16) | (key1 << 16)).value;
    key4 = ctypes.c_uint32((key1 >> 8)  | (key1 << 24)).value;
    #print '%x, %x, %x, %x'%(key1, key2, key3, key4)
    key = [key1, key2, key3, key4]

    fmt = '%a %b %d %H:%M:%S %Y UTC'
    if date == '':
        t = '%x'%time.time()
    else:
        tm = time.strptime(date, fmt)
        t = '%x'%time.mktime(tm)
        #print time.asctime(tm)

    v = struct.unpack('II', t)
    res = tea16b_encipher(v, key)
    resbin = struct.pack('II', res[0], res[1])
    
    digest = '0123456789abcdef'
    resstr = ''
    for i, b in enumerate(resbin):
        resstr += digest[ord(b) & 0x0f]
        resstr += digest[(ord(b) & 0xf0) >> 4]

    randstr = ''
    
    for i in range(8):
        randstr += digest[random.randint(0, 15)]

    return resstr + randstr
```
