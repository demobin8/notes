> 原样的笔记，估计大部分人看了也不知道这是啥，不改了都放出来。。。

tracker逆向记录
1、tracker ip来源，未从通信中找到相关报文，未从配置文件找到配置。
2、报文组成
iqiyi-tracker.pcap dspfmt(nodeinfos, 'h, b, ip, !port, ip, !port, ip')
short:    0 byte:  0 ip:  192.168.1.102 port: 7172 ip: 183.54.247.199 port: 7172 ip:   119.84.75.67 
short:11039 byte:  3 ip:  192.168.0.100 port: 7172 ip: 60.172.101.103 port: 7172 ip:  202.108.14.66 
short:11039 byte:  3 ip:  192.168.0.106 port: 7172 ip: 183.154.222.14 port:27348 ip:   119.84.75.66 
short:11039 byte:  5 ip:  192.168.1.145 port: 7172 ip:  183.57.83.193 port: 5492 ip:  113.107.99.11 
short:11039 byte:  6 ip:  192.168.1.130 port: 7172 ip:114.236.238.164 port:35767 ip:   119.84.75.66 
short:11039 byte:  5 ip:  192.168.1.103 port: 7172 ip: 221.204.162.39 port: 1507 ip:   112.90.35.81 
short:11039 byte:  6 ip:  192.168.1.106 port: 7172 ip:  218.64.21.191 port: 7172 ip:  113.107.99.11 
short:11039 byte:  6 ip:    192.168.1.3 port: 7172 ip:    36.62.57.17 port:22965 ip:   119.84.75.67 
short:11039 byte:  5 ip:  192.168.1.177 port: 7172 ip:  58.44.164.112 port: 7172 ip:   119.84.75.67 
short:11039 byte:  4 ip:  192.168.1.106 port: 7172 ip:    183.29.24.5 port: 7172 ip:  113.107.99.11 ...
183.54.147.199广东省深圳市 电信 
60.172.101.103安徽省黄山市 电信
183.154.222.14浙江省金华市 电信
183.57.83.193广东省佛山市 电信
114.236.238.164江苏省盐城市 电信
221.204.162.39山西省太原市 联通
218.64.21.191江西省南昌市 电信
36.62.57.17安徽省阜阳市 电信
58.44.164.112湖南省湘西土家族苗族自治州 电信
183.29.24.5广东省河源市 电信

IQYtrackerReq
```
uint32_t csum;
uint32_t number1;
uint16_t cmd;//1011
uint32_t pad1;
uint16_t pad2;
uint32_t datalen;// pktlen - 20
uint32_t count;
uint8_t  id[16];
uint8_t  hash[16];
```
IQYPeerInfo
```
uint32_t lanip;//host order
uint16_t port1;//host order
uint32_t wanip;//host order
uint16_t port2;
uint32_t stunip;
uint16_t delim;//2b1f
uint8_t  operator;
```
IQYTrackerRsp
```
uint32_t csum;
uint32_t number1;// = req.number1
uint16_t cmd;//1012
uint32_t pad1;//0
uint16_t pad2;//0
uint32_t datalen;// pktlen - 20
uint8_t  hash[16];// = req.hash
uint32_t count;
```
PeerInfo info[rsp.count];

3、破解csum算法过程，ida中先跑py脚本，得到LocalUdpServer_OnStart函数，进入后跟踪任意cmd的处理流程，第一步就是检测csum，发现和普通md5流程相比多了4个字节的一次md5update过程，OD跟踪得到该key即可。csum算法py版验证
```
def getiqiyicsum(src, ishex):
    if ishex:
        srchex = src[4:]
    else:
        srchex = binascii.a2b_hex(src)[4:]
    srchex += '\xe3\xbe\xa5\x54'
    m = hashlib.md5(srchex).digest()
    csum = struct.unpack('IIII', m)
    return csum[0]^csum[1]^csum[2]^csum[3]
```

重定向c范例
```
void iqiyi_tracker_handle_udp(struct packet *pkt)
{
	IQYTrackerReq *req = (IQYTrackerReq *)pkt->data;
	IQYTrackerRsp rsp = {'\0'};
	rsp.number1 = req->number1;
	rsp.cmd = 0x1210;
	rsp.datalen = sizeof(rsp) - 20;
	memcpy(rsp.hash, req->hash, sizeof(rsp.hash));
	rsp.count = 1;
	rsp.info.delim = 0x1f2b;
	rsp.info.operator = 2;
	rsp.info.lanip = inet_network("192.168.1.88");
	rsp.info.port1 = 51515;
	rsp.info.wanip = inet_network("192.168.1.88");
	rsp.info.port2 = 51515;
	//rsp.info.stunip = inet_network("119.84.75.67");
	rsp.info.stunip = 0;
	//memcpy((uint8_t *)&(rsp.info), iqiyi_info, sizeof(rsp.info));
	uint8_t data[1024] = {'\0'};
	memcpy(data, (uint8_t *)&rsp + 4, sizeof(rsp) - 4);
	memcpy(data + sizeof(rsp) - 4, "\xe3\xbe\xa5\x54", 4);
    	MD5_CTX ctx;
    	unsigned char hash[MD5_STR_LEN/2];
    	MD5_Init(&ctx);
    	MD5_Update(&ctx, (void *)data, sizeof(rsp));
    	MD5_Final(hash, &ctx);
	rsp.csum = (*((uint32_t *)&hash))^(*((uint32_t *)&hash[4]))^(*((uint32_t *)&hash[8]))^(*((uint32_t *)&hash[12]));
	udp_send_rsp_pkt(pkt, (uint8_t *)&rsp, sizeof(rsp));
}
```

4、如果wanip与lanip相同，stunip填0

Peer逆向记录
5、Peer报文结构
IQYPeerHSReq
```
uint32_t csum;
uint32_t number1;
uint16_t cmd;//1011
uint32_t pad1;
uint16_t pad2;
uint32_t datalen;// pktlen - 20
PeerInfo info;
uint8_t  hash[16];//
```
IQYPeerHSRsp
```
uint32_t csum;
uint32_t number1;
uint16_t cmd;//1011
uint32_t pad1;
uint16_t pad2;
uint32_t datalen;// pktlen - 20
PeerInfo info;
uint8_t  hash[16];
uint32_t num2;
uint16_t un;//ff0f
```
IQYPeerDataReq
```
uint32_t csum;
uint32_t number1;
uint16_t cmd;//1011
uint32_t pad1;
uint16_t pad2;
uint32_t datalen;// pktlen - 20
uint8_t  hash[16];
uint32_t offset;
uint32_t index;
```
IQYPeerDataRsp
```
uint32_t csum;
uint32_t number1;
uint16_t cmd;//1011
uint32_t pad1;
uint16_t pad2;
uint32_t datalen;// pktlen - 20
uint8_t  hash[16];
uint32_t offset;
uint32_t index;
uint32_t datalen;//0x0400
uint8_t  data;
```
