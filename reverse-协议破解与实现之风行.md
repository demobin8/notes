> 原样的笔记，估计大部分人看了也不知道这是啥，不改了都放出来。。。

```
#ifndef __FUNSHION_SERVER_H__
#define __FUNSHION_SERVER_H__
#include "common.h"

#define FS_HS_SYN		0x2100
#define FS_HS_ACK		0x2200
#define FS_CTL_ACK_1		0x2300
#define FS_CTL_ACK_2		0x2400
#define FS_DATA_REQ		0x2500
#define FS_DATA_RSP		0x2600

#pragma pack(push)
#pragma pack(1)
```
tracker服务器地址：ls.funshion.com, ls3.funshion.com
```
typedef struct _FSTrackerReqHdr
{
	uint32_t rand;//随机0x38414df2
	uint32_t len;//包长
	uint32_t fingerprint;//特征0x02007100
	uint16_t ordernum;//序号
	uint16_t unknown;//
	uint8_t  videohash[20];//哈希
	uint32_t clipsnum;
	uint8_t  peerid[20];//id  id组成0300D05400471200D8DF0800(uint32_t ip)(uint16_t port)FF97
	uint32_t wanip;//外网ip
	uint32_t localip;//内网ip
	uint32_t unknown2;
	uint32_t unknown3;
	uint32_t version;//版本号
	uint32_t unknown4;
}_FSTrackerReqHdr;

typedef struct _FSPeerInfo
{
	uint8_t  remoutePeerId[20];//peer id
	uint32_t wanip;//外网ip
	uint32_t locip;//内网ip
	uint16_t tcpport;//tcp外网传输端口
	uint16_t locport;//
	uint16_t udpport;//udp端口
	uint16_t location;//位置
	uint8_t  nattype;//nat类型
}FSPeerInfo;

typedef struct _FSTrackerRspHdr
{
	uint32_t rand;//req.rand
	uint32_t len;//包长
	uint32_t fingerprint;//特征0x02007100
	uint16_t ordernum;//req.ordernum
	uint16_t unknown;//0x0de3
	uint32_t unknown1;0x2c013c00
	uint32_t clipsnum;//0x24000000
	uint32_t unknown2;//0x22000000
	uint16_t unknown3;0x01800204
	uint8_t  unknown4;
	uint8_t  peerCnt;//peer总数
	FSTPeerInfo peer;
}_FSTrackerRspHdr;
```
秘钥
```
uint8_t key2[128];

void initKey2()
{
	key2[ 0   ] = 0xa6;
	key2[ 1   ] = 0xe2;
	key2[ 2   ] = 0x47;
	key2[ 3   ] = 0xdc;
	key2[ 4   ] = 0x0d;
	key2[ 5   ] = 0x70;
	key2[ 6   ] = 0x71;
	key2[ 7   ] = 0x21;
	key2[ 8   ] = 0x6d;
	key2[ 9   ] = 0x21;
	key2[ 10  ] = 0x28;
	key2[ 11  ] = 0xdd;
	key2[ 12  ] = 0xd1;
	key2[ 13  ] = 0x6d;
	key2[ 14  ] = 0x20;
	key2[ 15  ] = 0xa4;
	key2[ 16  ] = 0xac;
	key2[ 17  ] = 0x88;
	key2[ 18  ] = 0x0a;
	key2[ 19  ] = 0x75;
	key2[ 20  ] = 0xd5;
	key2[ 21  ] = 0x7f;
	key2[ 22  ] = 0x12;
	key2[ 23  ] = 0xd4;
	key2[ 24  ] = 0x8a;
	key2[ 25  ] = 0x26;
	key2[ 26  ] = 0x0a;
	key2[ 27  ] = 0x65;
	key2[ 28  ] = 0xb4;
	key2[ 29  ] = 0x52;
	key2[ 30  ] = 0xc4;
	key2[ 31  ] = 0xb9;
	key2[ 32  ] = 0x6c;
	key2[ 33  ] = 0x49;
	key2[ 34  ] = 0xbf;
	key2[ 35  ] = 0x68;
	key2[ 36  ] = 0xbf;
	key2[ 37  ] = 0x77;
	key2[ 38  ] = 0x06;
	key2[ 39  ] = 0x60;
	key2[ 40  ] = 0xae;
	key2[ 41  ] = 0x63;
	key2[ 42  ] = 0x56;
	key2[ 43  ] = 0x7c;
	key2[ 44  ] = 0x79;
	key2[ 45  ] = 0xe1;
	key2[ 46  ] = 0x7f;
	key2[ 47  ] = 0x59;
	key2[ 48  ] = 0x1e;
	key2[ 49  ] = 0x88;
	key2[ 50  ] = 0x0c;
	key2[ 51  ] = 0x65;
	key2[ 52  ] = 0x1c;
	key2[ 53  ] = 0x66;
	key2[ 54  ] = 0x26;
	key2[ 55  ] = 0x38;
	key2[ 56  ] = 0x7c;
	key2[ 57  ] = 0xf3;
	key2[ 58  ] = 0xb6;
	key2[ 59  ] = 0x28;
	key2[ 60  ] = 0x12;
	key2[ 61  ] = 0x44;
	key2[ 62  ] = 0xca;
	key2[ 63  ] = 0x17;
	key2[ 64  ] = 0x01;
	key2[ 65  ] = 0x81;
	key2[ 66  ] = 0x3a;
	key2[ 67  ] = 0x90;
	key2[ 68  ] = 0x7d;
	key2[ 69  ] = 0x99;
	key2[ 70  ] = 0x8b;
	key2[ 71  ] = 0x13;
	key2[ 72  ] = 0xd5;
	key2[ 73  ] = 0x34;
	key2[ 74  ] = 0x13;
	key2[ 75  ] = 0xac;
	key2[ 76  ] = 0xb0;
	key2[ 77  ] = 0xea;
	key2[ 78  ] = 0x5e;
	key2[ 79  ] = 0xca;
	key2[ 80  ] = 0x96;
	key2[ 81  ] = 0xb2;
	key2[ 82  ] = 0xd1;
	key2[ 83  ] = 0x4f;
	key2[ 84  ] = 0xb3;
	key2[ 85  ] = 0x9d;
	key2[ 86  ] = 0x8d;
	key2[ 87  ] = 0xe4;
	key2[ 88  ] = 0xd8;
	key2[ 89  ] = 0xc4;
	key2[ 90  ] = 0x97;
	key2[ 91  ] = 0x8f;
	key2[ 92  ] = 0xc3;
	key2[ 93  ] = 0x7e;
	key2[ 94  ] = 0x35;
	key2[ 95  ] = 0x87;
	key2[ 96  ] = 0xa0;
	key2[ 97  ] = 0xd7;
	key2[ 98  ] = 0x9b;
	key2[ 99  ] = 0x47;
	key2[ 100 ] = 0xd0;
	key2[ 101 ] = 0x3e;
	key2[ 102 ] = 0xc6;
	key2[ 103 ] = 0xe1;
	key2[ 104 ] = 0xe8;
	key2[ 105 ] = 0x7e;
	key2[ 106 ] = 0xa9;
	key2[ 107 ] = 0x95;
	key2[ 108 ] = 0xfd;
	key2[ 109 ] = 0xf0;
	key2[ 110 ] = 0x87;
	key2[ 111 ] = 0xa2;
	key2[ 112 ] = 0x1f;
	key2[ 113 ] = 0xee;
	key2[ 114 ] = 0xa0;
	key2[ 115 ] = 0x5c;
	key2[ 116 ] = 0x23;
	key2[ 117 ] = 0x8a;
	key2[ 118 ] = 0x0f;
	key2[ 119 ] = 0x7f;
	key2[ 120 ] = 0xa6;
	key2[ 121 ] = 0x80;
	key2[ 122 ] = 0xf3;
	key2[ 123 ] = 0xc3;
	key2[ 124 ] = 0x4e;
	key2[ 125 ] = 0x6a;
	key2[ 126 ] = 0xcd;
	key2[ 127 ] = 0xb0;
}
```
取出解密长度
```
int FSTDecodeSize(uint8_t *data)
{
	uint8_t index = 8 * (data[2]/16 & 0xf);	
	data[3] ^= key2[index];
	return data[3];
}
```
解密
```
int FSTDecode(uint8_t *data, int len)
{
	int i = 4; 
	uint32_t unknown = *((uint16_t *)data)<<16|*((uint16_t *)data);
	//int lenbak = 0xfffffffc & data[3];
	int lenbak = 32;
	int index = 8 * (*(uint8_t *)(data + 2)/16 & 0xf);
	while(i < lenbak)
	{
		while(index < 124 && i < lenbak)
		{
			*((uint32_t *)(data + i)) ^= unknown^(*(uint32_t *)(&key2[index]));
			i += 4;
			index += 4;
		}
		index = 0;
	}
}
```
TCP判断条件
```
	uint16_t port = ntohs(pkt->tcp_hdr.tcp_destination_port);
	if(pkt->data_len == 84 && (port == 8000 || port == 8080))
	{
		int num = FSTDecodeSize(pkt->data);
		FSTDecode(pkt->data, pkt->data_len);
		if(*(uint32_t*)&(pkt->data[8]) != 0x03000100)
			return;
		FSTHandleTcp(pkt);
```		
UDP判断条件
```
	int num = FSTDecodeSize(pkt->data);
	FSTDecode(pkt->data, pkt->data_len);
	if(*(uint32_t*)&(pkt->data[8]) != 0x03000100)
		return;
	FSTHandleUdp(pkt);
```
压缩
```
int encodeGz(uint8_t *data, int datalen, uint8_t *output, int outputlen)
{
	z_stream strm;
	strm.zalloc = Z_NULL;
	strm.zfree  = Z_NULL;
	strm.opaque = Z_NULL;

	strm.avail_in = datalen;
	strm.avail_out = outputlen;
	strm.next_in = data;
	strm.next_out = output;

	int err = -1;
	err = deflateInit2(&strm, Z_DEFAULT_COMPRESSION, Z_DEFLATED, MAX_WBITS + 16, MAX_MEM_LEVEL, Z_DEFAULT_STRATEGY);

	if (err == Z_OK)
	{
		err = deflate(&strm, Z_FINISH);
		if (err == Z_STREAM_END)
		{
			(void)deflateEnd(&strm);
			return outputlen - strm.avail_out;
		}
		else
		{
			(void)deflateEnd(&strm);
			printf("compression failed\n");
			return -1;
		}
	}
	else
	{
		(void)deflateEnd(&strm);
		printf("compression initialization failed\n");
		return -1;
	}
}	
```	
封包
```
unsigned char peer[] = {
	0x04, 0x01, 0xe5, 0x3e, 0x00, 0xc0, 0x12, 0x00, 0xed, 0xb8, 0x60, 0xa4, 0x4c, 0x2a, 0x10, 0x18, 
	0x0a, 0x9e, 0xc9, 0xb0, 0xc0, 0xa8, 0x00, 0xc7, 0xc0, 0xa8, 0x00, 0xc7, 0x00, 0x00, 0x00, 0x00, 
	0xc9, 0x3b, 0x00, 0x00, 0x09
};
	//FSPeerInfo peer = {'\0'};
	//peer.wanip = inet_addr("192.168.1.88");
	//peer.udpport = htons(51515);
	//peer.nattype = 9;
	FSTrackerReqHdr *req = (FSTrackerReqHdr  *)pkt->data;
	FSTrackerRspHdr resp = {'\0'};
	uint8_t buf[CHUNK] = {'\0'};
	int outputlen = encodeGz((uint8_t *)&peer, sizeof(peer), buf, sizeof(buf));
	//resp.rand = getrand(0xffffff)<<8 | 0x20;
	resp.rand = 0x20710ff8;
	resp.len = htonl(32 + outputlen);
	resp.fingerprint = 0x02007100;
	resp.ordernum = req->ordernum;
	resp.unknown = htons(0xe30d);
	resp.unknown1 = 0x2c013c00;
	resp.clipsnum = 0x24000000;
	resp.unknown2 = 0x22000000;
	resp.unknown3 = 0x0204;
	resp.unknown4 = 0x80;
	resp.peerCnt = 1;
	uint8_t *sendbuf = NULL;
	sendbuf = (uint8_t *)calloc((sizeof(resp) + outputlen), sizeof(uint8_t));
	memcpy(sendbuf, (uint8_t *)&resp, sizeof(resp));
	memcpy(sendbuf + sizeof(resp), buf, outputlen);
	FSTDecodeSize(sendbuf);
	FSTDecode(sendbuf, 32);
	udp_send_resp_pkt(pkt, sendbuf, sizeof(resp) + outputlen);
	free(sendbuf);
	sendbuf = NULL;
	
uint8_t key3[64];

void FSInitKey3()
{
	key3[0  ] = 0x0 ;
	key3[1  ] = 0x0 ;
	key3[2  ] = 0x0 ;
	key3[3  ] = 0x0 ;
	key3[4  ] = 0x0 ;
	key3[5  ] = 0x0 ;
	key3[6  ] = 0x0 ;
	key3[7  ] = 0x0 ;
	key3[8  ] = 0x0 ;
	key3[9  ] = 0x0 ;
	key3[10 ] = 0x0 ;
	key3[11 ] = 0x0 ;
	key3[12 ] = 0x0 ;
	key3[13 ] = 0x0 ;
	key3[14 ] = 0x0 ;
	key3[15 ] = 0x0 ;
	key3[16 ] = 0x0 ;
	key3[17 ] = 0x0 ;
	key3[18 ] = 0x0 ;
	key3[19 ] = 0x0 ;
	key3[20 ] = 0x0 ;
	key3[21 ] = 0x0 ;
	key3[22 ] = 0x0 ;
	key3[23 ] = 0x0 ;
	key3[24 ] = 0x0 ;
	key3[25 ] = 0x0 ;
	key3[26 ] = 0x0 ;
	key3[27 ] = 0x0 ;
	key3[28 ] = 0x0 ;
	key3[29 ] = 0x0 ;
	key3[30 ] = 0x0 ;
	key3[31 ] = 0x0 ;
	key3[32 ] = 0xC4;
	key3[33 ] = 0x1F;
	key3[34 ] = 0x14;
	key3[35 ] = 0x9C;
	key3[36 ] = 0xDF;
	key3[37 ] = 0x87;
	key3[38 ] = 0x24;
	key3[39 ] = 0x33;
	key3[40 ] = 0xE8;
	key3[41 ] = 0x4A;
	key3[42 ] = 0x3A;
	key3[43 ] = 0xA2;
	key3[44 ] = 0x42;
	key3[45 ] = 0x7C;
	key3[46 ] = 0xB1;
	key3[47 ] = 0x4E;
	key3[48 ] = 0x98;
	key3[49 ] = 0x21;
	key3[50 ] = 0xAD;
	key3[51 ] = 0x47;
	key3[52 ] = 0x0A;
	key3[53 ] = 0x13;
	key3[54 ] = 0xD3;
	key3[55 ] = 0xC4;
	key3[56 ] = 0xBC;
	key3[57 ] = 0x33;
	key3[58 ] = 0x3F;
	key3[59 ] = 0x8A;
	key3[60 ] = 0x5C;
	key3[61 ] = 0x26;
	key3[62 ] = 0x12;
	key3[63 ] = 0xCC;
}

int FSPeerEncode(uint8_t *data, int len, int key)
{
	int i = 0; 
	if(key == 0)
		key = *((uint16_t *)(data + 4));
	else
		*(uint16_t*)(data + 4) = key;

	for(i = 0; i < len; i += 2)
	{
		if(i < 6) continue;
		if(i >= 32) return 0;
		if(i + 2 > len)
		{
			//last one
			*((uint8_t *)(data + i)) ^= (uint8_t)(key & 0xff);
		}
		else
		{
			*((uint16_t *)(data + i)) ^=  key;
		}
	}
}

uint16_t FSA12Checksum(uint8_t *data)
{
	uint16_t sum = 0;
	for(int i = 0; i < 6; i++)
	{
		sum += ~(*(uint16_t *)(data + i * 2));
	}
	return sum - 2;
}

uint16_t FSGetKey(uint8_t *data)
{
	return *(uint16_t *)(data + 2) ^ *((uint16_t *)&key3[0] + 16 * (*(data + 1) & 0xF) + ((*(data + 1) >> 4) & 0xF));
}
```
视频信息获取url
"http://jobsff.funshion.com/query/v1/mp4/%s.json", %videohashstr
内容如下
```
{"return":"succ","client":{"ip":"120.39.25.34","sp":"0","loc":"0"},"playlist":[{"bits":"737280","tname":"dvd","size":"262458684","urls":["http:\/\/117.27.153.51:80\/play\/A42EF6E70164519017EFE01FB0601D46E4025C25.mp4","http:\/\/221.229.165.27:80\/play\/A42EF6E70164519017EFE01FB0601D46E4025C25.mp4","http:\/\/183.136.235.145:80\/play\/A42EF6E70164519017EFE01FB0601D46E4025C25.mp4","http:\/\/115.231.64.200:80\/play\/A42EF6E70164519017EFE01FB0601D46E4025C25.mp4","http:\/\/115.231.181.68:80\/play\/A42EF6E70164519017EFE01FB0601D46E4025C25.mp4","http:\/\/14.17.72.103:80\/play\/A42EF6E70164519017EFE01FB0601D46E4025C25.mp4","http:\/\/113.107.204.4:80\/play\/A42EF6E70164519017EFE01FB0601D46E4025C25.mp4","http:\/\/61.155.217.7:80\/play\/A42EF6E70164519017EFE01FB0601D46E4025C25.mp4","http:\/\/222.84.164.13:80\/play\/A42EF6E70164519017EFE01FB0601D46E4025C25.mp4"]}]}
```
字段含义
return表示查询结果，error失败succ成功
client表示发起查询的客户端信息，包括外网IP，和location
playlist, size为视频的大小
urls为视频的http地址

开始视频数据请求前的流程
client->server  FSPeerHSSynHdr
server->client  FSPeerHSAckHdr
client->server  FSPeerHSAckHdr

=====================================
client->server  FSPeerCtrlHSInfoReqHdr
server->client  FSPeerCtrlRspHdr
上下两个没有先后顺序
server->client  FSPeerCtrlHSInfoReqHdr
client->server  FSPeerCtrlRspHdr
=====================================

=====================================
client->server  FSPeerCtrlISInfoReqHdr
server->client  FSPeerCtrlRspHdr
上下两个没有先后顺序
server->client  FSPeerCtrlISInfoReqHdr
client->server  FSPeerCtrlRspHdr
=====================================

=====================================
client->server  FSPeerCtrlBitFieldReqHdr
server->client  FSPeerCtrlRspHdr
上下两个没有先后顺序
server->client  FSPeerCtrlBitFieldReqHdr
client->server  FSPeerCtrlRspHdr
=====================================
---------------------------------1------------------
```
typedef struct _FSPeerHSSynHdr
{
	uint16_t rand;//随机
	uint16_t unknown;//如果主动发出，填0x5031，否则req.unknown
	uint16_t key;  //getkey(data)
	uint16_t pktlen;//包长
	uint32_t fingerprint;//0x01011000
	uint16_t checksum;  //getchecksum(data)

	uint32_t cmd;	    //0x21
	uint8_t  padding;
	uint16_t seq;	    //如果主动发出，填0，否则req.seq+1
	uint32_t age;//不填
}FSPeerHSSynHdr;

typedef struct _FSPeerHSAckHdr
{
	uint16_t rand;//随机
	uint16_t unknown;//如果主动发出，填0x5031，否则req.unknown
	uint16_t key;//getkey(data)
	uint16_t pktlen;//包长
	uint32_t fingerprint;//0x01011000
	uint16_t checksum;	//getchecksum(data)

	uint32_t cmd;		//0x22
	uint8_t  padding;
	uint16_t seq;//如果主动发出，填0，否则req.seq+1
	uint32_t age;//不填
}FSPeerHSAckHdr;
```
--------------------------2--------client-peer------------------
```
uint8_t hs_info_req_unknown3[24] = {0xc5, 0x31, 0xc2, 0x77, 0xba, 0x68, 0x7f, 0xf4, 0x28, 0x13, 0x3e, 0x18, 0xd4, 0x78, 0x56, 0x1d, 0xed, 0x98, 0x35, 0x24, 0xd3, 0x7e, 0x6e, 0x87};
uint8_t hs_info_req_unknown4[24] = {0x1b, 0x9a, 0xa8, 0x57, 0xbf, 0x4e, 0x00, 0x00, 0xaa, 0x0b, 0x00, 0x00, 0x00, 0x00, 0x09, 0xbe, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00};
typedef struct _FSPeerCtrlHSInfoReqHdr
{
	uint16_t rand;//随机
	uint16_t unknown;//如果主动发出，填0x5031，否则req.unknown
	uint16_t key;//getkey(data)
	uint16_t pktlen;//包长
	uint32_t fingerprint;//0x01011000
	uint16_t checksum;//getchecksum(data)

	uint32_t cmd;//0x23
	uint8_t  padding;
	uint16_t seq;//如果主动发出，填0，否则req.seq+1
	uint32_t age;//不填

	uint8_t  unknown3[24]; //值为hs_info_req_unknown3
	uint8_t  unknown7;//0x8
	uint8_t  downloadrate;//下载速率，单位kb，可不填
	uint8_t  maxdownloadrate;//用户输入的最大下载速率，单位kb，可不填
	uint8_t  maxuploadrate;//用户输入的最大上传速率，单位kb，可不填
	uint8_t  videohash[20];//文件哈希
	uint8_t  peerid[20];//id
	uint8_t  totaltasks;//总任务数，可不填
	uint8_t  unknown12;
	uint8_t  unknown9;
	uint8_t  runningtasks;//正在进行的任务书，可不填
	uint8_t  uploadrate;//上传速率，单位kb，可不填
	uint8_t  unknown10;
	uint16_t unknown11;
	uint8_t  unknown4[24]; //值为hs_info_req_unknown3
	uint8_t  unknown5;
	uint8_t  winlen;  //0x80
	uint16_t unknown6;
}FSPeerCtrlHSInfoReqHdr;

typedef struct _FSPeerCtrlRspHdr
{
	uint16_t rand;//随机
	uint16_t unknown;//如果主动发出，填0x5031，否则req.unknown
	uint16_t key;//getkey(data)
	uint16_t pktlen;//包长
	uint32_t fingerprint;//0x01011000
	uint16_t checksum;//getchecksum(data)

	uint32_t cmd;//0x24
	uint8_t  padding;
	uint16_t seq;//如果主动发出，填0，否则req.seq+1
	uint32_t age;//不填
}FSPeerCtrlRspHdr;

typedef struct _FSPeerCtrlISInfoReqHdr
{
	uint16_t rand;//随机
	uint16_t unknown;//如果主动发出，填0x5031，否则req.unknown
	uint16_t key;//getkey(data)
	uint16_t pktlen;//包长
	uint32_t fingerprint;//0x01011000
	uint16_t checksum;//getchecksum(data)
	uint32_t cmd;	//0x23
	uint8_t  padding;
	uint16_t seq;//如果主动发出，则FSPeerCtrlHSInfoReqHdr.req.seq+1，否则req.seq+1
	uint32_t age;//不填
	uint32_t unknown3;//0x28000000
	uint32_t unknown4;//0x000000e0
	uint8_t  maxuploadrate;//用户输入的最大上传速率，单位kb，可不填
	uint8_t  uploadrate;//上传速率，单位kb，可不填
	uint8_t  fspseed;//1
	uint8_t  uploadpeercount;//上传连接的peer数
	uint8_t  maxglobaldownloadrate;//用户输入的最大下载速率，单位kb，可不填
	uint8_t  globaldownloadrate;//下载速率，单位kb，可不填
	uint8_t  taskdownloadrate;//当前任务的下载速率，单位kb，可不填
	uint8_t  fspdownloading;//下载，可不填
	uint16_t unknown5;
	uint8_t  downloadpeercount;//下载连接的peer数
	uint8_t  unknown8;
	uint32_t unknown7;//0x00010101
	uint8_t  padding4[20];
}FSPeerCtrlISInfoReqHdr;

typedef struct _FSPeerCtrlBitFieldReqHdr
{
	uint16_t rand;//随机
	uint16_t unknown;//如果主动发出，填0x5031，否则req.unknown
	uint16_t key;//getkey(data)
	uint16_t pktlen;//包长
	uint32_t fingerprint;//0x01011000
	uint16_t checksum;//getchecksum(data)
	uint32_t cmd;//0x23
	uint8_t  padding;
	uint16_t seq;//如果主动发出，填FSPeerCtrlISInfoReqHdr.req.seq+1，否则req.seq
	uint32_t age;//不填
	uint16_t padding2;
	uint8_t  unknown2;//请求下载，填01，吐出填FSPeerCtrlBitFieldReqHdr.req.unknown2
	uint8_t  unknown3;/请求下载，填39，吐出填FSPeerCtrlBitFieldReqHdr.req.unknown3
	uint8_t  unknown4;//请求下载，填25，吐出填FSPeerCtrlBitFieldReqHdr.req.unknown4
	uint8_t  unknown3;//请求下载，填ff，吐出填0xff
	uint8_t  unknown4;//请求下载，填fe，吐出填0xff
	uint8_t  unknown5[311];//请求下载，填0，吐出填0xff
	uint8_t  bitfield;//请求下载，填0，吐出填0xfc
}FSPeerCtrlBitFieldReqHdr;

typedef struct _FSPeerCtrlCheckReqHdr
{
	uint16_t rand;//随机
	uint16_t unknown;//如果主动发出，填0x5031，否则req.unknown
	uint16_t key;//getkey(data)
	uint16_t pktlen;//包长
	uint32_t fingerprint;//0x01011000
	uint16_t checksum;//getchecksum(data)
	uint32_t cmd;//0x23
	uint8_t  padding;
	uint16_t seq;//FSPeerCtrlBitFieldReqHdr.req.seq+1
	uint32_t age;//不填
	uint32_t ordernum1;//=req.ordernum1
	uint8_t  ordernum2;//大于req.ordernum2表示有 小于表示无
}FSPeerCtrlCheckReqHdr;

typedef struct _FSPeerCtrlReqHdr
{
	uint16_t rand;//随机
	uint16_t unknown;//如果主动发出，填0x5031，否则req.unknown
	uint16_t key;//getkey(data)
	uint16_t pktlen;//包长
	uint32_t fingerprint;//0x01011000
	uint16_t checksum;//getchecksum(data)
	uint32_t cmd;//0x23
	uint8_t  padding;
	uint16_t seq;//前一个req.seq+1
	uint32_t age;//不填
}FSPeerCtrlReqHdr;

typedef struct _FSPeerCtrlRspHdr
{
	uint16_t rand;//随机
	uint16_t unknown;//如果主动发出，填0x5031，否则req.unknown
	uint16_t key;//getkey(data)
	uint16_t pktlen;//包长
	uint32_t fingerprint;//0x01011000
	uint16_t checksum;//getchecksum(data)
	uint32_t cmd;//0x24
	uint8_t  padding;
	uint16_t seq;//req.seq
	uint32_t age;//不填
}FSPeerCtrlRspHdr;
```
视频数据请求的流程
客户端会连续发送0-4 piecesindex序号的五个包，此时远端peer响应0-ceil(req.piecesize/1350)个视频数据包
如果不是则远端peer响应对应序号的数据包
```
typedef struct _FSPeerDataReqHdr
{
	uint16_t rand;//随机
	uint16_t unknown;//如果主动发出，填0x5031，否则req.unknown
	uint16_t key;//getkey(data)
	uint16_t pktlen;//包长
	uint32_t fingerprint;//0x01011000
	uint16_t checksum;//getchecksum(data)
	uint32_t cmd;//0x25
	uint32_t seq;//起始0，之后递增
	uint32_t totalindex;//第几块
	uint32_t padding;
	uint32_t offset;//块的偏移
//total index, offset, piecesindex的算法
//每个index为40000h的数据，每个totalindex为一个piece，每个piece大小16384 = 1350*12 + 184，word  offset 网络字节序 为这个index的偏移，index * 40000h + offset = 完整的偏移
	uint16_t piecessize;//这个块的大小
	uint16_t piecesindex;//子块索引
	uint8_t  padding2;
	uint16_t left;//不填
}FSPeerDataReqHdr;

typedef struct _FSPeerDataRspHdr
{
	uint16_t rand;//随机
	uint16_t unknown;//req.unknown
	uint16_t key;//getkey(data)
	uint16_t pktlen;//包长
	uint32_t fingerprint;//0x01011000
	uint16_t checksum;//getchecksum(data)
	uint32_t cmd;//0x26
	uint32_t seq;//req.seq
	uint32_t padding;

	uint32_t totalindex;	//第几块
	uint32_t offset;	//块的偏移
	uint32_t padding2;	
	uint32_t piecesindex;	//子块索引
        uint8_t  data[];
}FSPeerDataRspHdr;


#pragma pack(pop)
void FSServerRecvDone(Packet *pkt);
void FSServerPktHandle(int *index);
void FSServerInit(void);
#endif
```
