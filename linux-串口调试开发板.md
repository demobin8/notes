> ...

### minicom

第一次 启动时：
即输入 minicom提示 错误。则 需： minicom -s
启动
出现配置菜单：选serial port setup
进入串口配置
输入A配置串口驱动为/dev/ttyS0
输入E配置速率为38400 8N1
输入F将 Hardware Flow Control 设 为 NO
回车 退出
由于我们使用minicom作为超级终端控制路由器等设备, 而不是控制modem, 所以需要修改Modem and dialing, 将Init string, Reset string, Hang-up string设置为空.
在配置菜单 选Save setup as df1保存（一定要记得这一步）
选Exit退出

下次在输入minicon 即可直接进入。
命令minicom是进入串口超级终端画面，而minicom -s为配置minicom。
说明/dev/ttyS0 对应为串口0 为你连接开发板的端口。

注意：非正常关闭minicom，会在/var/lock下创建几个文件LCK*，这几个文件阻止了minicom的运行，将它们删除后即可恢复

 

### kermit可以方便的发送内核或者U-BOOT等

apt-get install ckermit

vi ~/.kermrc

set line /dev/ttyS0
set speed 38400
set carrier-watch off
set handshake none
set flow-control none
robust
set file type bin
set file name lit
set rec pack 1000
set send pack 1000
set window 5
c

切回KERMIT， 先按CTRL+\再按C，连接输入C

 

较新的linux系统使用USB转串口不需要另外安装驱动

使用

lsmod | grep usbserial

命令可以查看是否支持

minicom的设置和普通串口差不多

唯一要改的是 /dev/ttyUSB0就可以了。
