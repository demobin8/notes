## [server] install
### 准备文件
从[https://wiki.asterisk.org/wiki/pages/viewpage.action?pageId=4817506](asterisk官网)下载如下软件包
asterisk-13-current.tar.gz
dahdi-linux-complete-current.tar.gz

### 安装软件包
sudo apt install vim make gcc pkg-config libavformat-dev ffmpeg libswscale-dev libvpx-dev sqlite3 libsqlite3-dev libssl-dev python-pip libv4l-dev alsa-base libasound2-dev libncurses5-dev uuid-dev libjansson-dev libxml2-dev
sudo pip install python-application Cython

### 配置
https://wiki.asterisk.org/wiki/display/AST/WebRTC+tutorial+using+SIPML5
https://wiki.asterisk.org/wiki/display/AST/Secure+Calling+Tutorial

mkdir /etc/asterisk/keys

### TroubleShooting
http://forums.asterisk.org/viewtopic.php?f=1&t=74253
```
echo "blacklist netjet" >> /etc/modprobe.d/dahdi.blacklist.conf
reboot
```

[asterisk] dial plan
```
[context]
exten => extensionnum,priority,action
```
### 构成
context名称，下一个[context]出现结束
extensionnum电话号码
priority优先级
action动作

### extensionnum
x,X     0-9
n,N     1-9
z,Z     2-9
.     任意字符和数字
[123]     1,2,3中的任意一个
_     含有任意通配符的表达式，都以_开头
s     start extension
t     timeout extension
i     invalid extension
h     hangup extension

### priority
n为next,即上面的priority+1
可以为priority定义名称，如n(name)

### action
-. Answer([delay])

-. Playback(filename[&filename2...][|option])

语音文件是相对地址也可以是绝对地址，相对地址的默认路径是/var/lib/asterisk/sounds/

-.Background(filename1[&filename2...][|options[|langoverride][|context]])

-.Dial(Technology/resource[&Tech2/resource2...][|timeout][|options][|URL])

options如下：

  -. A(x) ：当被叫方应答的时候给被叫方播放一段语音，x为要播放的语音文件
  
  -. C ：重新设置CDR
  
  -. d ：允许主叫方在等待被叫方应答的时候，按一个数字键跳转到这个数字所能匹配的流程中，新的流程是指定在EXITCONTEXT变量中设置的流程，如果EXITCONTEXT没有被指定那么就在当前context中寻找。
  
  -. D([called][:calling]) ：发送DTMF到主叫方或者被叫方，当被叫应答但是通道还没有桥接的时候。
  
  -. f ：强制为被叫方Channel设置CallerID，用当前的extension
  
  -. g ：当对方挂机的后，接着当前的context执行
  
  -. G(context^exten^pri) ：当呼叫被应答之后，将主叫方跳转到指定的priority中执行，被叫跳转到指定的priority+1中执行，指定的priority由G的参数指定。
  
  -. h ：允许被叫方按"*"结束会话
  
  -. H ：允许主叫方按"*"结束会话
  
  -. i ：忽略任何forwarding请求
  
  -. j ：当所有呼叫请求都忙的时候跳转到当前priority+101处
  
  -. k ：允许被叫使用parking功能
  
  -. K ：允许主叫使用parking功能
  
  -. L(x[:y][:z]) ：限定呼叫'x'ms，当剩下'y'ms时播放一个警告，重复这个警告每隔'z'ms。
  
  下面这些变量是用于这个操作：
  
  LIMIT_PLAYAUDIO_CALLER yes|no (default yes) 对主叫播放语音
  
  LIMIT_PLAYAUDIO_CALLEE yes|no 对被叫播放语音
  
  LIMIT_TIMEOUT_FILE 时间到的时候播放的语音
  
  LIMIT_CONNECT_FILE 呼叫开始时播放的语音
  
  LIMIT_WARNING_FILE y定义的那个警告的语音，一般都是播放还剩多少时间
  
  -. m([class]) ：为主叫提供hold music在Channel应答之前。
  
  -. M(x[^arg]) ：为被叫Channel执行指定的宏，在还未和主叫桥接之前。被指定的参数可以用"^"来分隔。宏执行完后后会返回一个变量MACRO_RESULT来指示接下来要执行的命令：
  
  ABORT 通话两端都挂断
  
  CONGESTION 当线路催挂的时候执行，也就是设置完CONGESTION状态，然后继续执行流程
  
  BUSY 当线路忙的时候执行，如果j这个参数被设置则，跳转到priority+101处执行
  
  CONTINUE 挂断被叫，主叫继续执行流程
  
  GOTO:<context>^<exten>^<priority> 跳转到指定的流程处继续执行
  
  注意：TIMEOUT()函数不能用在宏中
  
  -. n([x])和N ：修改screen/privacy模式. ；screen/privacy就是在被叫应答后还没有桥接之前给被叫播放一段IVR来让它做一些操作，其中就有选择是否愿意接受这个呼叫
  
  -. p和P([x]) ：设置screen/privacy模式.
  
  -. o ：指定主叫Channel的callerID为被叫Channel的CallerID。
  
  -. O([x]) ：设置Operator Services模式，只对zaptel和dahdi通道有效
  
  -. r ：主叫等待应答是为主叫播放回铃音
  
  -. S(x) ：应答后x秒挂断通话
  
  -. t ：允许被叫发送DTMF实现transfer主叫 详细信息在features.conf中设置
  
  -. T ：允许主叫发送DTMF实现transfer被叫 详细信息在features.conf中设置
  
  -. w ：允许被叫发送DTMF为通话录音 详细信息在features.conf中设置
  
  -. W ：允许主叫发送DTMF为通话录音 详细信息在features.conf中设置
  
-. Hangup([causecode])

