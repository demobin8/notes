> 从数据结构入手了，罗列了一下，但是没有说清楚。。。

### 0x01suricata的线程说明

* 抓包线程
* detect线程
等，可以参考tm-threads-common.h，顾名思义
```
typedef enum {
    TMM_DECODENFQ,//fq解码
    TMM_VERDICTNFQ,
    TMM_RECEIVENFQ,//fq抓包
    TMM_RECEIVEPCAP,//pcap抓包
    TMM_RECEIVEPCAPFILE,
    TMM_DECODEPCAP,
    TMM_DECODEPCAPFILE,
    TMM_RECEIVEPFRING,
    TMM_DECODEPFRING,
    TMM_DETECT,
    TMM_ALERTFASTLOG,
    TMM_ALERTFASTLOG4,
    TMM_ALERTFASTLOG6,
    TMM_ALERTUNIFIED2ALERT,
    TMM_ALERTPRELUDE,
    TMM_ALERTDEBUGLOG,
    TMM_ALERTSYSLOG,
    TMM_LOGDROPLOG,
    TMM_ALERTSYSLOG4,
    TMM_ALERTSYSLOG6,
    TMM_RESPONDREJECT,
    TMM_LOGHTTPLOG,
    TMM_LOGHTTPLOG4,
    TMM_LOGHTTPLOG6,
    TMM_LOGTLSLOG,
    TMM_LOGTLSLOG4,
    TMM_LOGTLSLOG6,
    TMM_PCAPLOG,
    TMM_FILELOG,
    TMM_FILESTORE,
    TMM_STREAMTCP,
    TMM_DECODEIPFW,
    TMM_VERDICTIPFW,
    TMM_RECEIVEIPFW,
#ifdef __SC_CUDA_SUPPORT__
    TMM_CUDA_MPM_B2G,
    TMM_CUDA_PACKET_BATCHER,
#endif
    TMM_RECEIVEERFFILE,
    TMM_DECODEERFFILE,
    TMM_RECEIVEERFDAG,
    TMM_DECODEERFDAG,
    TMM_RECEIVEAFP,
    TMM_DECODEAFP,
    TMM_ALERTPCAPINFO,
    TMM_RECEIVENAPATECH,
    TMM_DECODENAPATECH,
    TMM_SIZE,
} TmmId;

/*Error codes for the thread modules*/
typedef enum {
    TM_ECODE_OK = 0,    /**< Thread module exits OK*/
    TM_ECODE_FAILED,    /**< Thread module exits due to failure*/
    TM_ECODE_DONE,    /**< Thread module task is finished*/
} TmEcode;

/* ThreadVars type */
enum {
    TVT_PPT,
    TVT_MGMT,
    TVT_CMD,
    TVT_MAX,
};
```

### 0x02suricata的运行模式与线程的关系

* single
* worker
* autofp

待续。。。

### 0x03线程cpu亲和力

linux的线程数一般设为cpu核心数的2n + 1

在suricata配置中可以设置不同线程的cpu亲和力
```
 cpu-affinity:
   - management-cpu-set:
   ...
   - receive-cpu-set:
   ...
   - worker-cpu-set:
   ...
```

### 0x04线程模型数据结构
先来看一下线程在内存中的数据结构ThreadVars，是个双向链表，定义在threadvars.h中
```
/** \brief Per thread variable structure */
typedef struct ThreadVars_ {
    pthread_t t;//线程句柄
    char *name;//线程名称
    char *thread_group_name;

    SC_ATOMIC_DECLARE(unsigned char, flags);//状态

    /** aof(action on failure) determines what should be done with the thread
        when it encounters certain conditions like failures */
    uint8_t aof;

    /** the type of thread as defined in tm-threads.h (TVT_PPT, TVT_MGMT) */
    uint8_t type;

    /** no of times the thread has been restarted on failure */
    uint8_t restarted;

    /** queue's */
    Tmq *inq;//数据包输入队列
    Tmq *outq;//输出队列
    void *outctx;
    char *outqh_name;//输出队列名称

    /** queue handlers */
    struct Packet_ * (*tmqh_in)(struct ThreadVars_ *);//输入包handler
    void (*InShutdownHandler)(struct ThreadVars_ *);
    void (*tmqh_out)(struct ThreadVars_ *, struct Packet_ *);//输出包的handler

    /** slot functions */
    void *(*tm_func)(void *);
    struct TmSlot_ *tm_slots;//线程下的TmSlot，TmSlot关联TmModule

    uint8_t thread_setup_flags;
    uint16_t cpu_affinity; /** cpu or core number to set affinity to 亲和度*/
    int thread_priority; /** priority (real time) for this thread. Look at threads.h */

    /* the perf counter context and the perf counter array */
    SCPerfContext sc_perf_pctx;
    SCPerfCounterArray *sc_perf_pca;

    SCMutex *m;
    SCCondT *cond;

    uint8_t cap_flags; /**< Flags to indicate the capabilities of all the
                            TmModules resgitered under this thread */
    struct ThreadVars_ *next;
    struct ThreadVars_ *prev;
} ThreadVars;
```
TmSlot，定义在tm-threads.h中
```
typedef struct TmSlot_ {
    /* the TV holding this slot */
    ThreadVars *tv;//所属的线程

    /* function pointers */
    SC_ATOMIC_DECLARE(TmSlotFunc, SlotFunc);//处理包的函数指针，下面也是各种处理函数的指针

    TmEcode (*PktAcqLoop)(ThreadVars *, void *, void *);

    TmEcode (*SlotThreadInit)(ThreadVars *, void *, void **);
    void (*SlotThreadExitPrintStats)(ThreadVars *, void *);
    TmEcode (*SlotThreadDeinit)(ThreadVars *, void *);

    /* data storage */
    void *slot_initdata;
    SC_ATOMIC_DECLARE(void *, slot_data);

    /* queue filled by the SlotFunc with packets that will
     * be processed futher _before_ the current packet.
     * The locks in the queue are NOT used */
    PacketQueue slot_pre_pq;

    /* queue filled by the SlotFunc with packets that will
     * be processed futher _after_ the current packet. The
     * locks in the queue are NOT used */
    PacketQueue slot_post_pq;

    /* store the thread module id */
    int tm_id;

    /* slot id, only used my TmVarSlot to know what the first slot is */
    int id;

    /* linked list, only used when you have multiple slots(used by TmVarSlot) */
    struct TmSlot_ *slot_next;
} TmSlot;
```

TmModule，定义在tm-modules.h
```
/* thread flags */
#define TM_FLAG_RECEIVE_TM      0x01
#define TM_FLAG_DECODE_TM       0x02
#define TM_FLAG_STREAM_TM       0x04
#define TM_FLAG_DETECT_TM       0x08

typedef struct TmModule_ {
    char *name;

    /** thread handling */
    TmEcode (*ThreadInit)(ThreadVars *, void *, void **);
    void (*ThreadExitPrintStats)(ThreadVars *, void *);
    TmEcode (*ThreadDeinit)(ThreadVars *, void *);

    /** the packet processing function */
    TmEcode (*Func)(ThreadVars *, Packet *, void *, PacketQueue *, PacketQueue *);

    TmEcode (*PktAcqLoop)(ThreadVars *, void *, void *);

    /** global Init/DeInit */
    TmEcode (*Init)(void);
    TmEcode (*DeInit)(void);

    void (*RegisterTests)(void);

    uint8_t cap_flags;   /**< Flags to indicate the capability requierment of
                             the given TmModule */
    /* Other flags used by the module */
    uint8_t flags;
} TmModule;

TmModule tmm_modules[TMM_SIZE];
```
### 0x05线程队列
Tmq，定义在tm-queues.h中
```
typedef struct Tmq_ {
    char *name;//名称
    uint16_t id;//id
    uint16_t reader_cnt;//多少读
    uint16_t writer_cnt;//多少写
    /* 0 for packet-queue and 1 for data-queue */
    uint8_t q_type;//队列分类标志
} Tmq;
```
