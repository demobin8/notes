> 这里没有写后续，后续是分析看到了某个mod的关键字，是我们一个模块驱动的bug，改了就好了。。。

今天机房一台检测器系统崩溃了，同事让跟踪一下原因。

由于系统宕机无法用dmesg查看信息了，而且信息很多，屏幕显示不完整（宕机时无法shift+pageup查看屏幕上一页），看了两眼也看不出什么东西来，只好拍照存下来慢慢看，重启了。

回去研究oops信息的时候觉得这样不行，万一发现不了什么，而下次再出现还是没办法（以前做嵌入式时倒是可以通过串口查看到完整的oops信息），就给系统装了个linux-crashdump工具，等下次出现时就好分析了。

Kdump是一个比较通用的Linux内核崩溃转储程序，它的原理是在内存中保留一块区域用来存放内核发生crash后的capture kernel，通过kexec把保存的capture kernel运行起来，再由capture kernel把crash kernel的完整信息--包括CPU寄存器、堆栈数据等--转储到文件中。

`apt-get install linux-crashdump`

linux-crashdump包括三个工具，crash,kexec-tools,makedumpfile。

安装完之后可以在/boot/grub/grub.cfg中看到引导命令行后面多了如下内容：

```
linux   /boot/vmlinuz-3.0.0-12-server root=UUID=d516fa8e-635e-4349-a658-56b668d10ce1 ro   crashkernel=384M-2G:64M,2G-:128M
```

用service kdump status居然不支持，也不知道kdump服务会不会自启动，我就暂时先给它写到/etc/rc.local中了。

`service kdump start`

crash kernel默认保存在/var/crash中，本来怕文件太大想修改一下路径的，后来看了一下还有很多空间就算了。不过还是提一下吧，修改vmcore的位置要修改/etc/init.d/kdump和/etc/init/apport.conf两个文件，都是写死在脚本里的，没有用户配置。

测试一下吧

`echo c>/proc/sysrq-trigger`

重启，查看/var/crash/中生产了一个linux-image-3.0.0.0-12-server.0.crash的文件。

解压

`apport-unpack /var/crash/linux-image-3.0.0.0-12-server.0.crash /tmp`

crash分析。/user/lib/debug/boot/vmlinux-3.0.0.0-12-server文件是gdb内核用的要安装了dbgsys才有，dbgsys下载地址在http://ddebs.ubuntu.com/pool/main/l/linux/，一定要选和你系统一样版本的才行，查看系统版本命令cat /proc/version或者uname -a，查看发行版的版本命令是cat /etc/issue。

`crash /usr/lib/debug/boot/vmlinux-3.0.0.0-12-server /tmp/VmCore`

常用crash调试的命令解释（可以通过help命令查看所有的命令及其帮助）：
```
p 把表达式的值打印出来。

bt 查看调用堆栈。

bt + pid 列出相应的进程堆栈。
bt -f 列出所有堆栈里面数据。

list linked list。

log 打印kernel message buffer。

mod 加载调试符号，这样 sym 和whatis 命令就能正确解释我们自己模块里面自定义的结构等信息。

whatis 在符号表中查找数据，比如查看一个数据结构的成员。

struct 把某个地址当成一个结构解析出来。

dis 汇编。
```
