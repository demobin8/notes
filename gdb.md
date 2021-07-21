
(android)[https://developer.android.com/ndk/guides/standalone_toolchain.html?hl=zh-cn]

生成独立编译工具链
`./make-standalone-toolchain.sh --arch=x86 --platform=android-18 --install-dir=/home/demobin/android-x86-toolchain`

如需显示调用stdc++则必须链接`-lsupc++`，否则报错如下：
```
/tmp/ccEur1Qd.o:test.c:DW.ref.__gxx_personality_v0: error: undefined reference to '__gxx_personality_v0'
```

编译选项
`/home/demobin/android-x86-toolchain/bin/i686-linux-android-gcc -std=c99 -g -o test test.c -lhci_curl -lhci_tts -lhci_sys -lhci_tts_local_synth --sysroot=/home/demobin/data2/android-ndk-r13b/platforms/android-18/arch-x86/`

修改只读属性
```
/system/lib "Read-only file system"
adb remount
chmod 777 /system/lib
```

error: only position independent executables (PIE) are supported.
`-pie -fPIE`

warning: Architecture rejected target-supplied description
Remote 'g' packet reply is too long: 0000000010acf1be000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000abf1be00000000947af2b6100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
```
sudo apt install gdb-multiarch
gdb-multiarch
set architecture armv5te
//sudo apt install gdb-arm-none-eabi
//arm-none-eabi-gdb
```

目标：

在指定端口执行gdbserver

`gdbserver :9527 test`

查看内存段分布

`cat /proc/[pid]/maps | grep test`

找到基址，在加上readelf读到该main的偏移地址，得到下断点的位置

宿主：

转发
`adb forward tcp:9527 tcp:9527 `

设置库路径

`set solib-search-path /home/demobin/data2/android-ndk-r13b/platforms/android-18/arch-x86/usr/lib/`

每次step next输出要执行的指令

`set disassemble-next on`

开启汇编级别的单步调试

`set step-mode on`

连接远程调试端口

`target remote 127.0.0.1:9527`

设置系统路径

`set sysroot /home/demobin/data2/android-ndk-r13b/platforms/android-18/arch-x86`

```
b *[断点位置]
```

打印指定寄存器的字符串
```
x/s *(char **)($ebp + 4)
b单字节
h双字节
w四字节
g八字节
p *(char **)($ebp + 4)
x 十六进制
d 十进制
u 十六进制
o 八进制
t 二进制
a 十六进制
c 字符格式
f 浮点数格式
```

打印结构体成员的偏移
```
p &((struct node*)0)->next
```

找到fp的文件路径
```
p fp._fileno
readlink /proc/$self-pid/fd/$fp._fileno
```
