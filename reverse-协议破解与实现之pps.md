> 原样的笔记，估计大部分人看了也不知道这是啥，不改了都放出来。。。

fid->[FID]str
```
int __cdecl get_md5_str3(int a1, unsigned int a2, int a3)
{
  int v3; // ebx@1
  unsigned int v4; // ebp@1
  unsigned int v5; // esi@1
  int v6; // eax@1
  int v7; // edi@1
  signed int v8; // edx@3
  unsigned __int8 v9; // dl@3
  int result; // eax@8
  int v11; // [sp+10h] [bp-4h]@1
  unsigned int v12; // [sp+1Ch] [bp+8h]@1

  v3 = a3;
  v4 = a2;
  v5 = 0;
  v6 = 0;
  v7 = a1;
  v11 = a3;
  v12 = 0;
  if ( v4 )
  {
    while ( (unsigned int)v6 <= 3 )
    {
      v9 = (*(_BYTE *)(v5 + v7) >> (3 - v6)) & 0x1F;
      v6 = ((_BYTE)v6 - 3) & 7;
      if ( !v6 )
        goto LABEL_6;
LABEL_7:
      *(_BYTE *)v3++ = byte_127AD274[v9];
      v11 = v3;
      if ( v5 >= v4 )
      {
        result = a3;
        *(_BYTE *)v3 = 0;
        return result;
      }
    }
    v8 = 255 >> v6;
    v6 = ((_BYTE)v6 - 3) & 7;
    v9 = (*(_BYTE *)(v5 + v7) & (unsigned __int8)v8) << v6;
    if ( v5 < v4 - 1 )
    {
      v5 = v12;
      v7 = a1;
      v9 |= *(_BYTE *)(v12 + a1 + 1) >> (8 - v6);
      v3 = v11;
    }
LABEL_6:
    ++v5;
    v12 = v5;
    goto LABEL_7;
  }
  *(_BYTE *)a3 = 0;
  return a3;
}
```

疑似加密函数
sub_1238da80 

加密从第三个字节开始，前两个字节为包长
加密算法为
n > 2
data[n] ^= data[n - 1]
打印函数
sub_1226fa30
data offset 16 * 8 - 1
datalen 934, 3a6

1208b820
Impl@URC2_Info@CryptoPP@@VBlockCipher@@CryptoPP@@

sub_1238d3d0-->sub_1238d8b0-->sub_1238da80-->sub_1237a410-->sub_123cd220-->sub_1243ef80

sub_1213AF40-->sub_12154220

req
fileoffset
00e2182b4572eb16ba00000104ba4a1b0000000070580000000000000460fbdb67
4d645a
00e2182b4572eb16ba00000104ba4a1c00000000905800000000000004c0f6b741
58005a
00e2182b4572eb16ba00000104ba4a1d00000000c0580000000000000480ed6f93
58245a
00e2182b4572eb16ba00100104ba4a1e00000000f8580000000000000400dbdfbe
583c5a
00e2182b4572eb16ba00000104ba4a1f000000003c590000000000000400b6bf67
58585a
00e2182b4572eb16ba00000104ba4a2000000000805900000000000004006c7ffe
58905a

http://data.video.qiyi.com/v.ts
```
var videoUrl={code:"A00000",data:{"l":"http://117.25.148.151/v.ts","t":"CT|FuJian_XiaMen-220.160.189.27","s":"1","time":"1413103787","v":"2014-9-1 v3.0.9","z":"xiamen2_ct"}};
```
http://iplocation.geo.qiyi.com/cityjson
返回json格式数据如下
```
var returnIpCity = {"code":"A00000","data":{"ip":"218.85.113.96", "isp":"中国电信", "country":"中国大陆", "province":"福建", "city":"厦门", "isp_id":1, "country_id":145, "province_id":16, "city_id":16002, "location_id": 1016002}};
```
list3.pps.tv.iqiyi.com/pc/288256.xml.gz
返回xml.gz文件，解压数据如下

www.iqiyi.com/v_19rrnkly3c.html?vd

上面两个文件里都可以搜索tvid和vid获取数据如下

tvid = 319308300
vid = a9612eaf0f1d894a2037cf4c3c9e9c28

tvid标识一个视频
vid标识该视频不同的画质

然后打开
http://cache.video.qiyi.com/vp/319308300/a9612eaf0f1d894a2037cf4c3c9e9c28/?src=e9194cb155e14ceba4d63c185289b3c5
src值为任意
返回数据
```
{"aid":319308300,"bossStatus":0,"bt":-1,"ca":0,"cid":6,"controlInfo":"","ctgid":0,"dd":"http://data.video.qiyi.com/videos","dm":"http://meta.video.qiyi.com","dm3u8":"http://cache.m.iqiyi.com/dc/dt/","dts":"20141011113651","du":"http://data.video.qiyi.com/videos","et":-1,"exclusive":0,"lgd":1,"lgp":0,"ntvd":0,"nvid":"","onlineStatus":1,"platforms":["PC","PC_BAIDU","PC_BAIDU_SUB","PC_CARRIER_IQIYI","PC_APP","PAD","PAD_WEB_IQIYI","PHONE","PHONE_WEB_IQIYI","PHONE_CAS_IQIYI","TV"],"st":101,"t":1,"t3d":[{"vid":"","vtp":0,"tid":0}],"tht":2,"tkl":[{"id":1,"lid":1,"vs":[{"duration":5891,"bytes":0,"fid":"e984cd35831cc066da751df19d4799125eeaacb7","p2p":"","bid":96,"vid":"25253833902514e8fc54e022bc1604e7","mu":"/20141011/cc/d8/efef02419c51fe6f5cfc219b918672a0.xml","ps":0,"bif":"http://data.video.qiyi.com/videos/v0/20141011/cc/d8/63d3e0406d8aac1cd50708d2287a77d0.bif","bifsz":2032,"bmeta":"http://data.video.qiyi.com/videos/v0/20141011/cc/d8/b2076c11ba10bf4a0e66e2a0892d0086.pfvmeta","bmetasz":29417,"mp4hd":"http://data.video.qiyi.com/videos/v0/20141011/cc/d8/de852e545ec0856c0d883b81aa5c1c9b.mp4header","mp4hdsz":3318219,"mtaset":"http://data.video.qiyi.com/videos/v0/20141011/cc/d8/4e171bd3b92ad1311f5a083a1652d792.metaset","mtasetsz":41054,"fs":[{"msz":2675,"l":"/v0/20141011/cc/d8/294bb265cc2e66dc58b5aefc5823bb68.f4v","d":360785,"b":9884694},{"msz":2819,"l":"/v0/20141011/cc/d8/4730865779dc62f52722ad6283f121a1.f4v","d":359949,"b":9861663},{"msz":3071,"l":"/v0/20141011/cc/d8/ff81b285e88a9e6daee13faad35a13ed.f4v","d":360181,"b":9864685},{"msz":2747,"l":"/v0/20141011/cc/d8/32da1b1c403bdbb6910f65ea28a8ec18.f4v","d":359810,"b":9851300},{"msz":2927,"l":"/v0/20141011/cc/d8/e63be35bd5566b3716f4ef596dcf702b.f4v","d":360181,"b":9869987},{"msz":2891,"l":"/v0/20141011/cc/d8/0c7dd7d8eb2404c6ef96a2139b26d1a9.f4v","d":360367,"b":9874424},{"msz":3125,"l":"/v0/20141011/cc/d8/ccc0b0222c6e0d82b61bd0a8cc3f4f84.f4v","d":360228,"b":9878748},{"msz":2873,"l":"/v0/20141011/cc/d8/a852b9b9a7e4d668e0db57a54e19308b.f4v","d":360228,"b":9855765},{"msz":2675,"l":"/v0/20141011/cc/d8/4325eca6732a7b4f2d23e02489b3f830.f4v","d":360135,"b":9862507},{"msz":2081,"l":"/v0/20141011/cc/d8/f17ed4470e2d5d19be0343c5ebb7bfab.f4v","d":360088,"b":9872599},{"msz":1973,"l":"/v0/20141011/cc/d8/1369b552d12f764fefca44f534a3c1e0.f4v","d":359995,"b":9845608},{"msz":2045,"l":"/v0/20141011/cc/d8/aa2b2a3929dcb0f0109adfd3884195d6.f4v","d":360228,"b":9870472},{"msz":2153,"l":"/v0/20141011/cc/d8/e15bb2a650dcd53438cb028aa530a199.f4v","d":359856,"b":9856134},{"msz":2027,"l":"/v0/20141011/cc/d8/6dac3a3ae84ac216f55df90faa3fd959.f4v","d":359949,"b":9871490},{"msz":2135,"l":"/v0/20141011/cc/d8/b8fb6c9550923b7d4dd388a63209bad9.f4v","d":360228,"b":9871054},{"msz":2837,"l":"/v0/20141011/cc/d8/7dae1fce3c89a5b6686cc68a62c6520a.f4v","d":488402,"b":13388621}],"flvs":[]},{"duration":5890,"bytes":0,"fid":"cc7eb155ae2fb3495bc03a5d42c828fb4c0b0d2a","p2p":"","bid":2,"vid":"4128033a1bfabdec29e103ee2c2c356d","mu":"/20141011/5a/19/ae0a03c96081b914c4e45f7905ba25bc.xml","ps":0,"bif":"http://data.video.qiyi.com/videos/v0/20141011/5a/19/959c96d0e9111d5b675c40d27c9e7154.bif","bifsz":7504,"bmeta":"http://data.video.qiyi.com/videos/v0/20141011/5a/19/aa399800839764fae104b64e5ef78acb.pfvmeta","bmetasz":24449,"mp4hd":"http://data.video.qiyi.com/videos/v0/20141011/5a/19/f7b274c5de6c4b3b9315cb506bd349cb.mp4header","mp4hdsz":3892667,"mtaset":"http://data.video.qiyi.com/videos/v0/20141011/5a/19/58eef10133edd580a60fd20ddd91c581.metaset","mtasetsz":36086,"fs":[{"msz":2243,"l":"/v0/20141011/5a/19/4f157d7daa35d30753b21e94c2477354.f4v","d":360732,"b":39243010},{"msz":2567,"l":"/v0/20141011/5a/19/fc8289e630225dc38a59ffde110ce5d2.f4v","d":359896,"b":39123524},{"msz":2585,"l":"/v0/20141011/5a/19/e8b34fd42ad80aba8cecfdcc3ab584d3.f4v","d":360128,"b":39166961},{"msz":2603,"l":"/v0/20141011/5a/19/a16146d65fda4c1fb9f709ad38b8368d.f4v","d":359757,"b":39133607},{"msz":2657,"l":"/v0/20141011/5a/19/4259da84a5557f0a9891da182e0ea601.f4v","d":360128,"b":38929402},{"msz":2603,"l":"/v0/20141011/5a/19/f3b11941da8fdd1266cd9e456927aecb.f4v","d":360314,"b":39127076},{"msz":2567,"l":"/v0/20141011/5a/19/d6bc5f5ef97d720f25f27e38819d5ad4.f4v","d":360175,"b":39245810},{"msz":2639,"l":"/v0/20141011/5a/19/657ceee5d706b7602aa0dd9e02d37011.f4v","d":360175,"b":39073157},{"msz":2189,"l":"/v0/20141011/5a/19/a0f112d2217f05653956fbb23c721e3c.f4v","d":360082,"b":39121770},{"msz":1955,"l":"/v0/20141011/5a/19/05530e09015dc6ad7126733c37c09203.f4v","d":360035,"b":39051204},{"msz":1847,"l":"/v0/20141011/5a/19/5a4095a09aabe5ee989a1906cd6a0543.f4v","d":359942,"b":38065938},{"msz":1847,"l":"/v0/20141011/5a/19/89c57201cffe8436249da5c383154020.f4v","d":360175,"b":38827306},{"msz":1919,"l":"/v0/20141011/5a/19/7a5b22c320617b70fc02d2523db3106c.f4v","d":359803,"b":39001214},{"msz":1793,"l":"/v0/20141011/5a/19/eaab10db6d956dcca62de307ef4dc617.f4v","d":359896,"b":39134508},{"msz":1829,"l":"/v0/20141011/5a/19/ccb269089ad96b913f5ba61add3e68ac.f4v","d":360175,"b":39074043},{"msz":2243,"l":"/v0/20141011/5a/19/d41d56557be0b05d431ae5ac4a524960.f4v","d":488349,"b":53151780}],"flvs":[]},{"duration":5890,"bytes":0,"fid":"c7c4892f9ae9df37bd9202f390f121eac244ade5","p2p":"","bid":4,"vid":"0c1e687fb7e6dca1fe843da906c4d70f","mu":"/20141011/bd/d7/fbaf5e8b81e07bb3b24a7221933bad40.xml","ps":0,"bif":"http://data.video.qiyi.com/videos/v0/20141011/bd/d7/8e6a2ef12f0aca25e6b1097b762722de.bif","bifsz":13360,"bmeta":"http://data.video.qiyi.com/videos/v0/20141011/bd/d7/35d8980106f874b12838dc1aecd13dff.pfvmeta","bmetasz":24432,"mp4hd":"http://data.video.qiyi.com/videos/v0/20141011/bd/d7/301f00be09eabd91a9f56816a61b41d8.mp4header","mp4hdsz":3910964,"mtaset":"http://data.video.qiyi.com/videos/v0/20141011/bd/d7/2a2db29b172a549fb030d3a1a2449721.metaset","mtasetsz":36084,"fs":[{"msz":2244,"l":"11-7c-1f-49-7b-1d-4-7d-49-51-78-4a-54-7a-18-4-7b-1a-3-2b-4d-57-7f-1c-5f-7e-4f-2-2a-48-5f-71-4b-52-2d-41-48-7f-1d-48-2c-1b-48-79-48-57-79-4d-56-78-4b-48-78-f-48","d":360732,"b":70797133},{"msz":2532,"l":"11-7c-1f-49-2d-4c-56-2a-4f-4-7a-41-5f-29-1a-57-7b-4d-55-78-1d-55-71-1b-51-7f-1f-55-2d-4f-50-2e-48-53-7b-1f-48-7f-1d-48-2c-1b-48-79-48-57-79-4d-56-78-4b-48-78-f-48","d":359896,"b":70607475},{"msz":2550,"l":"11-7c-1f-49-78-49-4-7e-18-5-2e-1c-55-2b-4d-1-78-49-2-2c-4d-52-7f-4b-57-2a-4f-55-78-18-56-79-4b-57-7e-1f-48-7f-1d-48-2c-1b-48-79-48-57-79-4d-56-78-4b-48-78-f-48","d":360128,"b":70907555},{"msz":2586,"l":"11-7c-1f-49-2d-4b-57-7e-1b-4-7e-49-5f-7f-1f-56-78-4e-5f-2a-4b-6-7e-41-1-7a-1c-51-2e-4e-50-2a-1c-5-2a-4b-48-7f-1d-48-2c-1b-48-79-48-57-79-4d-56-78-4b-48-78-f-48","d":359757,"b":70555997},{"msz":2676,"l":"11-7c-1f-49-70-1b-6-2c-4f-6-70-1b-5-7d-1a-3-2c-48-57-7e-41-56-79-41-54-2b-18-51-2e-4a-50-2a-4b-6-78-1f-48-7f-1d-48-2c-1b-48-79-48-57-79-4d-56-78-4b-48-78-f-48","d":360128,"b":69908454},{"msz":2622,"l":"11-7c-1f-49-70-18-4-7f-40-54-7d-4b-50-79-1b-6-7b-4e-57-7a-41-6-78-4e-5-2a-1d-6-7e-4f-4-70-1f-54-70-48-48-7f-1d-48-2c-1b-48-79-48-57-79-4d-56-78-4b-48-78-f-48","d":360314,"b":70017116},{"msz":2622,"l":"11-7c-1f-49-29-1a-3-2c-1c-1-7b-4e-5f-7b-48-5-7c-4e-1-7c-4f-5f-2a-1a-2-7f-4a-3-7d-40-51-2e-48-54-2e-49-48-7f-1d-48-2c-1b-48-79-48-57-79-4d-56-78-4b-48-78-f-48","d":360175,"b":70778438},{"msz":2622,"l":"11-7c-1f-49-2b-1f-52-7b-49-50-7f-1b-3-29-4d-4-7a-4c-50-7b-40-56-2d-18-3-78-41-54-2a-1d-2-78-18-4-78-4f-48-7f-1d-48-2c-1b-48-79-48-57-79-4d-56-78-4b-48-78-f-48","d":360175,"b":70391120},{"msz":2190,"l":"11-7c-1f-49-78-48-2-2c-1f-1-2d-40-57-2b-4d-57-7e-40-5f-2d-4a-3-2b-1c-2-78-4a-1-79-4a-5-29-49-50-2e-4a-48-7f-1d-48-2c-1b-48-79-48-57-79-4d-56-78-4b-48-78-f-48","d":360082,"b":70495573},{"msz":1938,"l":"11-7c-1f-49-2e-48-54-2d-1d-1-2c-4b-6-7b-4d-54-70-1a-53-79-4e-2-29-49-6-79-18-4-2d-40-53-2a-1d-3-29-1d-48-7f-1d-48-2c-1b-48-79-48-57-79-4d-56-78-4b-48-78-f-48","d":360035,"b":70529002},{"msz":1848,"l":"11-7c-1f-49-78-4b-57-78-40-5f-2a-1b-5e-2e-4c-1-7b-1c-52-2b-1f-4-7c-4a-53-70-41-5e-70-4f-57-7c-1b-51-2e-1c-48-7f-1d-48-2c-1b-48-79-48-57-79-4d-56-78-4b-48-78-f-48","d":359942,"b":68694097},{"msz":1848,"l":"11-7c-1f-49-7c-4f-5e-29-4b-1-7f-48-3-29-4a-5e-2e-1b-55-71-49-6-7c-41-6-71-1c-2-2c-4e-55-7a-4d-3-71-1b-48-7f-1d-48-2c-1b-48-79-48-57-79-4d-56-78-4b-48-78-f-48","d":360175,"b":70193113},{"msz":1938,"l":"11-7c-1f-49-2d-4b-6-7d-4f-5e-7c-48-57-70-4c-4-2e-1b-5f-2b-40-57-2d-4f-5f-2b-4f-52-7d-1b-55-70-40-5-7f-49-48-7f-1d-48-2c-1b-48-79-48-57-79-4d-56-78-4b-48-78-f-48","d":359803,"b":70339448},{"msz":1794,"l":"11-7c-1f-49-2e-4a-6-2a-48-53-7a-4d-51-2a-41-51-7c-48-54-2a-49-4-7a-1f-5e-78-4a-2-7c-4d-4-7c-40-57-2b-41-48-7f-1d-48-2c-1b-48-79-48-57-79-4d-56-78-4b-48-78-f-48","d":359896,"b":70746535},{"msz":1830,"l":"11-7c-1f-49-2a-48-4-70-18-5f-7e-1d-5e-7c-48-51-7c-1a-51-7e-1b-5-2d-4a-5e-2b-41-6-70-1d-53-7f-41-6-7c-41-48-7f-1d-48-2c-1b-48-79-48-57-79-4d-56-78-4b-48-78-f-48","d":360175,"b":70546745},{"msz":2244,"l":"11-7c-1f-49-2a-1d-55-2b-1b-2-7b-4f-4-78-4d-2-7c-49-52-70-1c-54-78-1b-55-78-4c-4-79-1d-54-79-4b-1-78-1d-48-7f-1d-48-2c-1b-48-79-48-57-79-4d-56-78-4b-48-78-f-48","d":488349,"b":95780614}],"flvs":[]},{"duration":5890,"bytes":0,"fid":"619295aa18f4487bc680da1e83249b0dc35aa29e","p2p":"","bid":1,"vid":"a9612eaf0f1d894a2037cf4c3c9e9c28","mu":"/20141011/38/0e/2441dd808159497e4b9eff5ceb02b541.xml","ps":0,"bif":"http://data.video.qiyi.com/videos/v0/20141011/38/0e/1a28e30106c586802bf33fed72ca1592.bif","bifsz":3736,"bmeta":"http://data.video.qiyi.com/videos/v0/20141011/38/0e/cff7f3e302aa6fb750d130a0e0eb76ce.pfvmeta","bmetasz":27275,"mp4hd":"http://data.video.qiyi.com/videos/v0/20141011/38/0e/d73453af43b456028959b1346c3f98e5.mp4header","mp4hdsz":3882919,"mtaset":"http://data.video.qiyi.com/videos/v0/20141011/38/0e/ccd2c5c654e18b5f7aa61c02c4a5b3a9.metaset","mtasetsz":38912,"fs":[{"msz":2549,"l":"/v0/20141011/38/0e/eaec0e360429a2d29004613cfe0928d0.f4v","d":360732,"b":18965543},{"msz":2693,"l":"/v0/20141011/38/0e/32bfdcd2278fe68b458636ae2d1c07a4.f4v","d":359896,"b":18943528},{"msz":2981,"l":"/v0/20141011/38/0e/1d69245f5bee44c8e8838c02c7c45391.f4v","d":360128,"b":19021146},{"msz":2801,"l":"/v0/20141011/38/0e/8cf1403de4d36f7f7093b3d5fb9b660a.f4v","d":359757,"b":18930340},{"msz":2747,"l":"/v0/20141011/38/0e/4b4cf01ab26c7399930581b90e916fd3.f4v","d":360128,"b":18905569},{"msz":2783,"l":"/v0/20141011/38/0e/217b418af78002cc4a543c149a4bf0d3.f4v","d":360314,"b":18971211},{"msz":2909,"l":"/v0/20141011/38/0e/8313cb07256e3c074633c3c8a2774867.f4v","d":360175,"b":18993734},{"msz":2765,"l":"/v0/20141011/38/0e/8f92bb9a8794c30660739f17af068363.f4v","d":360175,"b":18976042},{"msz":2513,"l":"/v0/20141011/38/0e/91a4227bb5d88e1ecc6c2c892e4ece8b.f4v","d":360082,"b":18956048},{"msz":1991,"l":"/v0/20141011/38/0e/65b2edd8a579d99c59520fe7b7ec4844.f4v","d":360035,"b":18957604},{"msz":1937,"l":"/v0/20141011/38/0e/9e1f385b0460ba9e14f67195be3089de.f4v","d":359942,"b":18862770},{"msz":1901,"l":"/v0/20141011/38/0e/d801be023ecdd2792ebd13b608ea07f6.f4v","d":360175,"b":19079532},{"msz":2009,"l":"/v0/20141011/38/0e/8e72e7a81c388047bc3e34a9e8947fe4.f4v","d":359803,"b":18897337},{"msz":1901,"l":"/v0/20141011/38/0e/4600d4727a7d7d15de0f61f6b35f78f0.f4v","d":359896,"b":18994006},{"msz":1937,"l":"/v0/20141011/38/0e/e6f8ab7990aaca5eb45a6164427c3d18.f4v","d":360175,"b":18967545},{"msz":2495,"l":"/v0/20141011/38/0e/bad97291fbab855c6c9c783f8d48e5c8.f4v","d":488349,"b":25724826}],"flvs":[]}],"vsext":[],"ispre":1}],"tsl":[{"stm":660,"etm":0,"stp":""},{"stm":1563,"etm":0,"stp":""}],"tvid":319308300,"uid":0,"up":"2014-10-11 11:36:51","ver":"01"}
```
l中的文件名 即为该文件的MD5值

key_1 = %d%s%s floor(time.time()/600) ")(*&^flash@#$%a" hashid
key_2 起始值01234567 89abcdef fedcba98 76543210
说明是md5算法

上报文中的fid既为peer handshake中的fid

key = md5(key_1)
http://data.video.qiyi.com/`key/videos/`l

http://data.video.qiyi.com/05553f03335a34a2d3d900e0ac2bb841/videos/v0/20140912/f4/03/129081d13770f0c1bdbf4225fd34d945.f4v?ran=1776&qyid=672b36fcf13ffd53d9c1bdf55f0e0b43&qypid=288864000_11&ran=1776

http://121.205.88.92/videos/v0/20140912/f4/03/129081d13770f0c1bdbf4225fd34d945.f4v?key=ea15e7a3d24ff5be&ran=1776&qyid=672b36fcf13ffd53d9c1bdf55f0e0b43&qypid=288864000_11&ran=1776&uuid=da5573a3-541aae49-27

.pfvmeta
http://pdata.video.qiyi.com/`key/videos/`url/
结果中会有url

根据ppslog-1的记录,tracker 36.250.67.53 返回48个节点的信息
分析对应的报文，可知包长为1231的包为负载该信息所在的报文
继续分析可知，每个节点的信息长度为20字节，初步分析，基本格如下

nodeinfo
```
uint32_t fingerprint //1483010b 主机序0x0b018314
uint32_t ip // net order
uint16_t tcpport // host order
uint16_t udpport // host order
uint8_t  padding1
uint8_t  unknown1 // ref cnt?
uint16_t padding2
uint8_t  unknown2 // 0x02 operator?
uint16_t un3 // city code?
uint8_t  pad
```

节点信息前一个字节为节点个数
第一二个字节为包长

当第二个字节为0x80是 只有第一个字节是指包长

tracker info req
```
uint16_t pktlen // 6400 0x64 100
uint16_t cmd1 // 4474 0x7444
uint8_t  cmd2 // 0x71
uint8_t  unid1[8] // dd59cf28782f3509
uint32_t un1[9] // 0b000000 00000000 0x14
uint8_t  fid[20]//79faa0ce 3a1987d0 776ddc47 12fa25be c85cf49e
uint32_t un2[15] // 00009c01 00000101 00000c28 010000 
uint32_t locip // net order
uint16_t locport // net order
uint8_t  un3[16] // 04000000 00004800 0000ffff 00000000
uint16_t un4
uint8_t  pad[9]
uint8_t  ppsstr[8] //'PPStream'
uint8_t  pad2[2]
```
trakcer info rsp
```
uint16_t pktlen
uint16_t cmd1 // 5575 0x7555
uint8_t  cmd2 // 0x17
uint8_t  unid1[8] // req.unid1
uint32_t un11 // 7b020000
uint32_t pad11 // 00000000
uint8_t  idlen // ? 0x14
uint8_t  fid[20] //req.unid2
uint8_t  un2[11] //00001100 00001a1a 1a1a 0a
uint8_t  nodecnt
nodeinfo node // nodeinfo*nodecnt 
uint8_t  un3[5] //fe78ff46 14
uint8_t  pad[20] 
uint32_t un41 // xxxxxx42
uint32_t un42 // xxxxxx43
uint32_t un43 // xxxxxx42
uint32_t un44 // xxxxxx42 
uint8_t  pad2[8]
uint32_t un5
uint32_t un6
uint32_t un7
uint32_t un8
uint32_t un9
uint32_t pad10
uint8_t  un11 //0x14
uint8_t  un12[20]
uint8_t  un13 //0x8b
uint8_t  pad3[4]
uint32_t un14 //08004001 0x01400008
uint8_t  pad4[7]
uint32_t un15
uint32_t pad5
uint32_t un16 //8b000000 0x8b
uint8_t  un17[7] //
uint8_t  pad6[5]
uint8_t  un18[41]
```
tracker ka req  
```
uint16_t pktlen // 5000 0x50 80
uint16_t cmd1 // 5572 0x7255
uint8_t  cmd2 // 0x71
uint32_t pad
uint32_t un1
uint32_t un2 // 03000000 0x03
uint32_t pad2
uint8_t  idlen // ? 0x14
uint8_t  id[20] // 
uint16_t un3
uint8_t  un4[8] // 00000101 00000c28
uint8_t  un5 //
uint8_t  un6[8] // 01000000 01001900
uint32_t locip // net order
uint16_t locport // net order
uint32_t un7
uint8_t  un8[9] // 04000000 00004800 f0
```
tracker ka rsp
```
uint16_t pktlen // 7700 0x77 119
uint16_t cmd1 // 4473 0x7344
uint8_t  cmd2 // 0x17
uint32_t pad
uint32_t un1 // req.un1
uint32_t un2 // 07000000 0x07
uint32_t pad2
uint8_t  idlen // ? 0x14
uint8_t  id[20] // req.id
uint8_t  un3[6] // 19000240 0200
uint8_t  un4 
uint16_t un5 // 4614
uint8_t  pad2[20]
uint32_t un6 // xxxxxx42
uint32_t un7 // xxxxxx43
uint32_t un8 // xxxxxx42
uint32_t un9 // xxxxxx42
uint8_t  pad3[8]
uint32_t un10
uint32_t un11
uint32_t un12
uint32_t un13
uint32_t un14
uint32_t pad4
```
peer hs req
```
uint8_t  pktlen // 0x8d 141
uint16_t fingerprint // 8000 0x80
uint16_t cmd // 1100
uint8_t  unid1[8] //
uint32_t un3 // 0100ff02 0x02ff0001
uint16_t locport // host order 1970 0x7019
uint8_t  fid[20] 
uint8_t  un4[18] //0c00ffff 0000ffff 00000000 00200000 4014
uint8_t  un5[20] // 0800 27c3ff97 d9e1dbd9 1eaaed40 7975a58 903fa
uint32_t locip
uint16_t pad2
uint32_t un6
uint8_t  un7[8] // 04000000 00004800 
uint16_T un8; // 090b
uint8_t  un9[30] // 00000001 00000000 000000d6 d0b9fa00 bbaab6ab 00b8a3bd a800cfc3 c3c5 
uint8_t  un10 // 7c 
uint8_t  un11[5] // b5523715 c5
uint32_t un12 
uint32_t pad3
```

peer hs rsp
```
uint8_t  pktlen // 0x90 144
uint16_t fingerprint // 8000 0x80
uint16_t cmd // 1200
uint8 _t unid1[8] // req.unid1
uint32_t un3 // 0100ff03 0x03ff0001
uint16_t locport
uint8_t  fid[20] // req.fid
uint8_t  un4[18] // req.un4
uint8_t  un5[20]
uint32_t locip
uint16_t pad2
uint32_t un6
uint8_t  un7 //req.un6  04000000 00004800 
uint8_t  un8 // 090f
uint8_t  un9[30] // 00000001 00000000 000100d6 d0b9fa00 bbaab6ab 00b8a3bd a800b8a3 d6dd
uint8_t  un10 // 08
uint8_t  un11[5] // b5523715 c5
uint8_t  pad3
uint8_t  un12[5] // 01647e16 0d
uint32_t pad4
```
peer data req
```
uint8_t  pktlen // 0x25 37
uint16_t fingerprint // 8000 0x80
uint16_t cmd // 2500
uint8_t  unid[8] 
uint32_t un3 // 00000104 0x04010000
uint16_t locport // net order
uint32_t index // 08000000
uint16_t offset // 00400100
uint32_t pad2
uint16_t datasize //  0040 0x0400
uint32_t un5
```
peer data rsp
```
uint8_t  un1
uint16_t fingerprint // 8400 
uint16_t cmd // 2600
uint8_t  unid[8] // req.unid
uint32_t un3 // 00004102 0x02410000
uint16_t locport // b375 port 30131
uint32_t pieceid // piece data md5? 每个piece为0x10个0x400 一个piece 16384字节
如7ba6fbeb 的offset包括 017c00 017800 017400 017000 016c00 016800 016400 016000 015c00 015800 015400 015000 014c00 014800 014400 014000
uint32_t index // 08000000
uint32_t offset // 00040100 每次递增400h
uint32_t pad //
uint16_t datasize // 0004 0x400
uint8_t  data[1024]
uint32_t un
```
peer un req
```
uint8_t  pktlen
uint16_t fingerprint // 8000
uint16_t cmd // 3100
uint8_t  unid[8] // 
uint32_t un3 // 01000300
uint16_t locport // 1970
uint32_t locip // c0a800c6
uint32_t un1
uint32_t un3
```
peer un rsp
```
uint8_t  pktlen
uint16_t fingerprint // 8000
uint16_t cmd // 2100
uint8_t  unid[8] //req.unid
uint32_t un3 // 02000200
uint16_t locport // f549 port 18933
uint8_t  un[5] // 01000000 0f
```
pfvmeta开头

mp4header结尾

fid可能会改变 vid不变 其他文件都是md5作为文件名


http://cache.video.qiyi.com/vp/319578400/ad4b002464ead7b827a12d69222ee8d8/
