> 不知道其他大佬是不是这么玩的。。。我猜做外挂的跟我这个流程类似。。。

在协议逆向过程中，肯定难免有协议字段分析困难的地方，可能字段含义不明朗，也可能加密了。

一般来说下断点有send,recv,sendto,recvfrom,WSAsend,WSARecv,WSASendto,WSARecvFrom这几个地方。

如何确定这几个函数呢，我常用的方法是使用封包助手，WPE我也用过，但是感觉支持的接口没用封包助手多，使用方法就是程序跑起来，封包助手抓包找到你要分析的报文，封包助手会显示出它使用的接口名。

找到接口之后bp下断，但是由于环境复杂，可能会断到很多次，这个时候你先看看你的报文的长度，看看是不是有一定的规律，比如定长或者大于多少小于多少，然后定位到retn之前，下条件断点，最常用的比如长度，EAX==19，或者[ebp+4] == feba等等。

如果断到想要的报文之后，你可以尝试执行到返回，如果是单线程，那之后应该就是代码处理流程了，比如解密、校验、解压等等。但是如果是多线程，那你可以在报文数据出下硬件断点或内存访问断点，报文数据就是传进来的参数，参数在ebp-4依次为1、2、3参数，硬件断点下好之后继续执行，断到之后执行到返回跟踪，一般就能找到处理的流程了。
