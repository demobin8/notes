> 这一章似乎也没写完。。。现在看的话，似乎太细了，没有给出高维视角的分析，很枯燥

这一章只大概介绍suricata的流程，各个模块的分析会在后面各个章节中完成。

从入口suricata.c:main()开始

...略

RunModeRegisterRunModes();

注册运行模式，运行模式的区别会再后面讲到，跟踪可以看到这函数里面的各种模式注册函数主要就是给static RunModes runmodes[RUNMODE_MAX];这个全局变量赋值。
```
while((opt = getopt_long(argc, argv, short_opts, long_opts, &option_index)) != -1){

...

}
```
循环解析启动参数，设置运行模式run_mode等全局变量的值。
```
...

if(ConfYamlLoadFile(conf_filename) != 0){

...

}
```
跟踪代码可以看到，这里载入并解析yaml配置文件，并将解析的结果保存在全局变量ConfNode *root中，而且配置文件是可以用include嵌套的。
```
...

AppLayerDetectProtoThreadInit();
```
这个函数调用了RegisterAppLayerParsers();，跟踪进去
```
...

RegisterHTPParsers();

RegisterSSLParsers();

...
```
大家应该都对FTP协议比较熟悉，我们就以FTP协议跟踪看一下这个注册函数的作用
```
...

AlpProtoAdd(&alp_proto_ctx, protoname, IPPROTO_TCP, ALPROTO_FTP, "USER", 5,0,STREAM_TOSERVER);
```
看变量命名这个函数的作用应该很容易理解，就是把协议识别注册到系统中。

alp_proto_ctx是一个AlpProtoDetectCtx类型的全局变量，其中成员AlpProtoSignature *head保存了每个协议的特征码、协议号等。

protoname就是协议名，这里就是FTP。

“USER”是FTP协议的特征码，suricata通过它来识别协议（如何进行模式匹配识别该特征码后面的章节会介绍），这也是它和snort的区别之一（为什么要用字符串来识别协议呢？因为现在的检测系统大多通过端口识别协议，很多协议或者说黑客发起会话并不希望被识别出来就会改变端口，但通常如果通信双方要通信必然要遵循某种格式也就是协议，比如RFC要求FTP协议的登录命令就是USER，当然suricata也支持用端口识别协议）。

STREAM_TOSERVER也很好理解，就是指客户端发往服务端的包（这里提一下，suricata中以发起会话的一端作为客户端）。

ALPROTO_FTP就是协议号，它的定义在app-layer-protos.h中。
```
...

AppLayerRegisterProto(proto_name, ALPROTO_FTP, STREAM_TOSERVER, FTPParseRequest);
```
该函数把ALPROTO_FTP协议的解析函数注册到系统中，FTPParseRequest就是一个回调函数，当会话是STREAM_TOSERVER时就把包交给它处理。

到此我们可以想到，如果我们要添加自己的应用层协议解析流程的话，仿上写好register并添加到RegisterAppLayerParsers();即可。
```
...

if(ConfGet("default-log-dir", &log_dir) ！= 1)｛

...

｝
```
ConfGet函数和接下来的ConfGetInt都是从之前解析好的root中获取某些配置项的值，并进行处理。如这里就是判断配置文件中指定的输出日志路径是否存在，如果不存在则退出。很多参数的处理都涉及到后面的模块的运行方式，这里就不一一解释了，之后遇到需要在回头来看。
```
...

SigTableSetup();

...

TmqhSetup();
```
注册多线程调度模块的队列处理函数，这会在之后的线程调度章节详细介绍，先只大概说一下，抓包线程会将抓到的包输出到一个队列中作为detect线程的输入队列进行处理。
```
...

SigParsePrepare();
```
预处理pcre
```
...

TmModuleReceivePcapFileRegister();

...
```
这里有很多的线程注册函数，我们就以pcapFile的注册函数跟踪看一下。

tmm_modules[TMM_RECEIVEPCAPFILE].name = "ReceivePcapFile";

tmm_modules是一个TmModule的全局数组，它保存了每个线程的线程明，初始化函数，包处理函数等等。

...

tmm_modules[TMM_RECEIVEPCAPFILE].PktAcqLoop = ReceivePcapFileLoop;

这个就是抓包函数，可以跟踪这个函数，它主要无限循环调用pcap_dispatch接口取包，如果是日志线程则为空。
```
...

tmm_modules[TMM_RECEIVEPCAPFILE].Func = NULL;
```
Func是包处理函数，如果是抓包线程则为空。
```
...

UtilSignalHandlerSetup(SIGINT, SignalHandlerSigint);
```
向系统注册自定义信号处理函数，这里是处理ctrl+c的信号。
```
...

PacketPoolInit(max_pending_packets);
```
max_pending_packets是前面从yaml配置文件中读取出来的配置参数，如果没有设置的话默认是1024.

这个函数顾名思义就是初始化报文池(这个名字是我随便起的)，报文池其实就是一个报文的缓冲区，那为什么要用池技术来做呢。很简单，和线程池技术一样，为了减少内存碎片，提高性能。

抓包线程获取了很多的报文，每个包由一个pakcet结构体保存在内存中，如果每个结构体内存都有内核申请释放，这样就会在内存链中产生很多1500左右大小并且不连续的内存，假设释放了某个内存段上下头的内存，中间某些内存没有释放，这样内核在分配大块内存时这些释放的内存还是没法使用，而且我们的分配释放的内存快是非常多也非常快的，必然会产生内存碎片，而且低效。

而池技术就解决了这些问题，它提前申请了一定数量的packet内存，一个packet不再使用就把它重置一下交给下一个packet使用，这样不仅防止了内存碎片也提高了性能。
```
PacketPoolStorePacket(p);

RingBufferMrMwPut(ringbuffer, (void *)p);
```
这个ringbuffer是一个全局变量，定义就在tmqh-packetpool.c: static RingBuffer16 *ringbuffer = NULL;

ringbuffer意思是一个环形缓冲区，
```
...

DetectEngineCtx *de_ctx = DetectEngineCtxInit();
```
初始化检测引擎的上下文，即初始化de_ctx结构体，Detect EngineCtx这个数据结构很重要，在后面会详细介绍，这里说一下就是不能把它和之后出现的DetectEngineThreadCtx* det_ctx混淆了。它是保存整个检测引擎的相关数据结构的，后面的是保存线程的相关数据结构的。
```
...

RunModeDispatch(run_mode, runmode_custom_mode, de_ctx);
```
这个函数很重要，在前面从命令行参数获取了suricata的运行模式之后，会通过这个函数根据不同模式分别创建不同的线程。

我们来跟一下这个函数
```
...

mode->RunModeFunc(de_ctx);
```
可以看到mode是就是从前面提到的全局变量runmodes中注册的，我们再返回之前的运行模式注册函数看看

以void RunModeIdsPcapRegister(void)；为例
```
RunModeRegisterNewRunMode(RUNMODE_PCAP_DEV, "autofp",
                              "Multi threaded pcap live mode.  Packets from "
                              "each flow are assigned to a single detect thread, "
                              "unlike \"pcap_live_auto\" where packets from "
                              "the same flow can be processed by any detect "
                              "thread",
                              RunModeIdsPcapAutoFp);
void RunModeRegisterNewRunMode(int runmode, const char *name,
                               const char *description,
                               int (*RunModeFunc)(DetectEngineCtx *))
```
可以看出上面mode->RunModeFunc(de_ctx);跑的就是RunModeIdsPcapAutoFp了，跟进来
```
ret = RunModeSetLiveCaptureAutoFp(de_ctx,
                              ParsePcapConfig,
                              PcapConfigGeThreadsCount,
                              "ReceivePcap",
                              "DecodePcap", "RxPcap",
                              live_dev);

int RunModeSetLiveCaptureAutoFp(DetectEngineCtx *de_ctx,
                              ConfigIfaceParserFunc ConfigParser,
                              ConfigIfaceThreadsCountFunc ModThreadsCount,
                              char *recv_mod_name,
                              char *decode_mod_name, char *thread_name,
                              const char *live_dev)
```
阅读代码，这个函数获取了cpu的个数，这是为了下面创建Detect线程做准备，Detect线程个数thread_max = ncpus * threading_detect_ratio。

先创建抓包抓包线程（这里的抓包线程不是说这个线程只抓包，它也包含它Decode处理的，这个将线程调度介绍吧）
```
ThreadVars *tv_receive =
                TmThreadCreatePacketHandler(thread_name,
                        "packetpool", "packetpool",
                        queues, "flow", "pktacqloop");
```
再创建Detect线程
```
ThreadVars *tv_detect_ncpu =
            TmThreadCreatePacketHandler(thread_name,
                                        qname, "flow",
                                        "packetpool", "packetpool",
                                        "varslot");
```
继续跟踪进入TmThreadCreate函数，原型
```
ThreadVars *TmThreadCreate(char *name, char *inq_name, char *inqh_name,
                           char *outq_name, char *outqh_name, char *slots,
                           void * (*fn_p)(void *), int mucond)
```
name线程的名字，inq_name输入队列的名字，inqh_name输入队列处理函数的名字，outq_name输出队列的名字，outqh_name输出队列处理函数的名字，slots这个我也不知道怎么用中文表述。。。

太多了，线程调度那一章再讲吧，继续主流程。
```
...

FlowManagerThreadSpawn();
```
会话管理线程，在suricata中，所有应用层协议都是针对会话进行处理的，所以必须有一个管理线程将不同会话的包分配给处理该会话的Detect线程。
```
if (delayed_detect) {
        if (SigLoadSignatures(de_ctx, sig_file, sig_file_exclusive) < 0) {
```
这个函数载入所有的策略。

待续。
