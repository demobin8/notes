> 零几年的笔记了，当时写在百度空间，现在百度空间都没了10年了。。。

### 0x01如何安装／卸载软件？

源码安装

./configure && make && make install

经验：如果提示缺少xxx.h头文件时，一般需要安装libxx-dev库，这时按普通软件的安装方式

apt-get install software_to_install

apt-get install支持tab补全，双击tab会弹出补全列表，选择你认为适合的即可，如果不是libxxx打头搜索不到，则你可能需要执行

apt-cache search xxx查找所有相关的软件，如果还没有则apt-get update更新系统软件库

### 0x2如何查看网卡，判断网卡状态？

ifconfig -a查看所有网卡，为RUNNING的网卡才是已启用的网卡

### 0x03如何自动获取ip？

dhcpclient eth0使eth0通过dhcp协议从dhcp服务器自动获取ip

### 0x04如何设置ip？

ifconfig eth0 192.168.1.101这种方式重启消失，如果要重启生效则通过vi编辑/etc/network/interfaces文件设置静态ip

```
auto eth0 

iface eth0 inet static 

address 192.168.1.101

netmask 255.255.255.0 

gateway 192.168.1.1 
```

再通过vi编辑/etc/resolv.conf添加dns域名解析服务器地址

`nameserver 192.168.1.1（或者8.8.8.8）`

0x05如何查看／添加／删除路由？

route -n查看所有路由

`route add／del -net 192.168.2.0 gw 192.168.1.1 netmask 255.255.255.0`添加通往2网段的路由

### 0x06如何查看网络流量？

`apt-get install nload`

nload左右键切换网卡，可以直观的查看网络流量

### 0x7如何查看具体的软件消耗的流量？

`apt-get install nethogs`

`nethogs eth0`

### 0x08如何查看哪个软件占用了哪个端口？

`lsof -i:8080`

### 0x09如果网络出错，如何排查？

1、查看网卡是否启动，工作是否正常

2、查看是否缺少dns，先查看ip，ping网关，如正常ping www.baidu.com

3、查看ip是否冲突，先查看ip，再ifdown eth0关闭网卡，ifconfig eth0 192.168.1.222重设ip，ping 原来的ip，如果通则ip冲突

4、查看是否路由出错，如果多个网卡工作在同一个网段，并因为前一条路由的网卡不工作，则删除该条路由，或者ifdown该网卡

5、查看是否iptables设置

### 0x10如何查看有哪些终端连这本机？

`w`

### 0x11如何发消息给所有／指定终端？

发给所有终端

`echo "who are u?" | wall`

发给指定终端

write root pts/0两个参数，第一个是username第二个是终端号，都可以通过w查看到

### 0x12如何踢掉指定终端？

`pkill -kill -t pts/2`

### 0x13如何查看有哪些终端曾经连接／尝试连接过本机？

 grep "Failed password " /var/log/auth.log

### 0x14如何查看本机开启了哪些服务？

`service --status-all`

### 0x15如何关闭开启／某些服务并开机子启动？

关闭`service ssh stop/start`

自启动`update-rc.d ssh start`

### 0x16如何查看定时任务？

crontab -l

如果定时任务直接存放在/var/spool/cron/crontabs/目录下，则通过crontab -l无法查看

### 0x17如何查看／杀死进程？
```

ps aux查看所有进程

ps aux|grep process_name

top查看最耗资源的进程

kill -9 pid杀死进程

pidof process_name显示pid

top -H -p pid具体到线程显示资源使用
```

### 0x18如何在不知道密码的情况下进入系统并修改root密码？

启动电脑，等待GRUB菜单，如果GRUB菜单隐藏，可以按Esc调出，如果设置了GRUB密码，按p解锁，按e在启动前编辑启动参数，选择kernel /boot/vmlinuz-2.6.12-8-386 root=/dev/hda2 ro quiet splash，按e编辑选定的启动菜单项，在参数最后添加rw init=/bin/bash，ctrl+x启动，进入系统passwd修改密码。 

### 0x19如何查看asc码？

`man ascii`

### 0x20如何快速在两个目录切换？

cd不加参数回到主目录

cd -返回上次目录

### 0x21如何批量删除所有包含指定字符串的文件？

```
rm `grep -r "string" ./ | awk -F : '{print $1}'`
```

### 0x22如何批量删除所有在指定时间之前的旧文件？

删除十天之前的文件

`find ./ -mtime +10 -name "*.*" -exec rm -Rf {} \;`

### 0x23如何批量删除所有大于指定大小的大文件？

`find . -type f -size +10M -exec rm -vf {} \;`

### 0x25如何在tar打包时不打包.svn目录？

`tar -zcf src.tar.gz src --exclude=.svn`
这个在移动svn工作目录时可能有用。
