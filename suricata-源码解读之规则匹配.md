> 多模匹配就开始涉及到算法了，当时也没看懂原理。。。

https://redmine.openinfosecfoundation.org/projects/suricata/wiki/Suricata_Rules

### prefilter

单条规则的匹配，就是数值比对

匹配的优先级原则等规则
```
    DetectSidRegister();
    DetectPriorityRegister();
    DetectRevRegister();
    DetectClasstypeRegister();
    DetectReferenceRegister();
    DetectTagRegister();
    DetectThresholdRegister();
    DetectMetadataRegister();
    DetectMsgRegister();
    DetectAckRegister();
    DetectSeqRegister();
    DetectContentRegister();
    DetectUricontentRegister();
    DetectPcreRegister();
    DetectDepthRegister();
    DetectNocaseRegister();
    DetectRawbytesRegister();
    DetectBytetestRegister();
    DetectBytejumpRegister();
    DetectSameipRegister();
    DetectL3ProtoRegister();
    DetectIPProtoRegister();
    DetectWithinRegister();
    DetectDistanceRegister();
    DetectOffsetRegister();
    DetectReplaceRegister();
    DetectFlowRegister();
    DetectWindowRegister();
    DetectRpcRegister();
    DetectFtpbounceRegister();
    DetectIsdataatRegister();
    DetectIdRegister();
    DetectDsizeRegister();
    DetectFlowvarRegister();
    DetectFlowintRegister();
    DetectPktvarRegister();
    DetectNoalertRegister();
    DetectFlowbitsRegister();
    DetectEngineEventRegister();
    DetectIpOptsRegister();
    DetectFlagsRegister();
    DetectFragBitsRegister();
    DetectFragOffsetRegister();
    DetectGidRegister();
    DetectMarkRegister();
    DetectCsumRegister();
    DetectStreamSizeRegister();
    DetectTtlRegister();
    DetectTosRegister();
    DetectFastPatternRegister();
    DetectITypeRegister();
    DetectICodeRegister();
    DetectIcmpIdRegister();
    DetectIcmpSeqRegister();
    DetectDceIfaceRegister();
    DetectDceOpnumRegister();
    DetectDceStubDataRegister();
    DetectHttpCookieRegister();
    DetectHttpMethodRegister();
    DetectHttpStatMsgRegister();
    DetectTlsRegister();
    DetectTlsVersionRegister();
    DetectUrilenRegister();
    DetectDetectionFilterRegister();
    DetectHttpHeaderRegister();
    DetectHttpRawHeaderRegister();
    DetectHttpClientBodyRegister();
    DetectHttpServerBodyRegister();
    DetectHttpUriRegister();
    DetectHttpRawUriRegister();
    DetectAsn1Register();
    DetectSshVersionRegister();
    DetectSslStateRegister();
    DetectSshSoftwareVersionRegister();
    DetectHttpStatCodeRegister();
    DetectSslVersionRegister();
    DetectByteExtractRegister();
    DetectFiledataRegister();
    DetectPktDataRegister();
    DetectFilenameRegister();
    DetectFileextRegister();
    DetectFilestoreRegister();
    DetectFilemagicRegister();
    DetectFileMd5Register();
    DetectFilesizeRegister();
    DetectAppLayerEventRegister();
    DetectHttpUARegister();
    DetectLuajitRegister();
    DetectIPRepRegister();
```
### mpm
通过函数PatternMatchPreparePopulateMpm构建上下文
```
static int PatternMatchPreparePopulateMpm(DetectEngineCtx *de_ctx,
                                          SigGroupHead *sgh)
```
通过函数PopulateMpmHelperAddPatternToPktCtx添加pattern
```
static void PopulateMpmHelperAddPatternToPktCtx(MpmCtx *mpm_ctx,
                                                DetectContentData *cd,
                                                Signature *s, uint8_t flags,
                                                int chop)
```
算法包括
```
ac|hs|ac-bs|ac-ks
```
