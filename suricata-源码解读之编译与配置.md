> 当时想对suricata的源代码做一个完整的解读系列笔记。。。版本都还是1.4，应该是全网独一份了，现在都到5.x了，代码笔记也是一大堆

### 0x01编译

suricata的源代码可以从http://suricata-ids.org/download/处免费获得，目前最新的版本是2.0beta(即测试)版，我们以stable(即稳定)版本1.4进行分析。

我的环境：linux发行版kali1.0x86。

从解压解压
```
tar xf suricata-1.4.tar.gz

cd suricata-1.4

automake

autoconf

./configure
```
报错
```
checking for yaml_parser_initialize in -lyaml... no
```
提示缺失libyaml-dev，安装之
```
apt-get install libyaml-dev

./configure
```
报错
```
configure: error: pcap.h not found ..
```
应该是缺失libpcap-dev（这里很多新手会迷茫，说没提示不知道该装什么，这里教大家一个小技巧：打开shell的自动补全，就是注释.bashrc的最后相关complete的几行即可，然后输入apt-get install libpcap并双击tab键，一般来说找一个libxxx-dev的即可）
```
apt-get install libpcap-dev

./configure
```
通过（碰到什么问题欢迎留言或私信探讨）

`make`

报错
```
../../src/suricata-common.h:204:21: fatal error: htp/htp.h: 没有那个文件或目录
```
```
cd libhtp

chmod +x configure

./configure

make;make install

cd ..

make;make install
```
OK，完成
```
cp suricata.yaml /usr/local/etc/suricata/

suricata -c /usr/local/etc/suricata/suricata.yaml -i eth0
```
如果报错文件threshold.config、reference.config不存在的话，创建目录并拷贝当前目录的这两个文件过去即可。

### 0x02configure参数

(下面的参数并不是一定要设置的，你可以不设置任何参数，就按上面的操作即可。)

./configure -h查看所有的参数

* DIR相关 如--bindir=DIR生成的可执行文件的路径等参数比较好理解就不说了。

* Program Names相关

    --program-prefix=PREFIX指定可执行程序的名字。

* System Types相关

    --build=BUILD编译的系统构架 --host=HOST目标构架，这两个是交叉编译时用的。

* Optional 相关

    --enable-unittests      Enable compilation of the unit tests将单元测试的代码也编译进去。

    --enable-debug          Enable debug output开启DEBUG模式的输出。suricata的DEBUG打开会打印很多很多很多。

    --enable-pfring         Enable Native PF_RING support开启pfring支持，打开这个选项你必须安装PFRING模块，PFRING的安装比较复杂，请查看官方文档，完成后用pfring的tcpdump抓包测试是否安装成功，如果在configure时指定了这个选项，那么你在启动suricata时也要加上--pfring-int=eth0选项。

* ENV相关，这个一般来说是通用的，CC编译器指令CFLAGS编译选项LDFLAGS链接选项LIBS链接库的路径。

### 0x03 启动参数

suricata -h查看启动参数
```
    -c <path>                    : path to configuration file配置文件，及上述的yaml文件
    -T                           : test configuration file (use with -c)测试一下yaml文件有没有出错
    -i <dev or ip>               : run in pcap live mode网卡名
    -F <bpf filter file>         : bpf filter file
    -r <path>                    : run in pcap file/offline mode读包模式，后跟文件名
    -s <path>                    : path to signature file loaded in addition to suricata.yaml settings (optional)规则文件路径，这个在yaml文件中是有配置的，也可以在命令行指定
    -S <path>                    : path to signature file loaded exclusively (optional)
    -l <dir>                     : default log directory日志的输出路径，这个也是在yaml中有配置的
    -D                           : run as daemon后台模式运行
    --list-runmodes              : list supported runmodes显示所有支持的运行模式
    --runmode <runmode_id>       : specific runmode modification the engine should run.  The argument
                                   supplied should be the id for the runmode obtained by running以和种模式运行，后跟list查看到的ID
                                   --list-runmodes
    --engine-analysis            : print reports on analysis of different sections in the engine and exit.
                                   Please have a look at the conf parameter engine-analysis on what reports
                                   can be printed
    --pidfile <file>             : write pid to this file (only for daemon mode)在后台模式下时把pid写入文件
    --init-errors-fatal          : enable fatal failure on signature init error
    --dump-config                : show the running configuration
    --pcap[=<dev>]               : run in pcap mode, no value select interfaces from suricata.yaml
    --pcap-buffer-size           : size of the pcap buffer value from 0 - 2147483647
    --af-packet[=<dev>]          : run in af-packet mode, no value select interfaces from suricata.yaml
    --erf-in <path>              : process an ERF file
```
Wireshark Cookie Dump:
