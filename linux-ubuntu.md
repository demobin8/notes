### fstab
```
/dev/sdb6 /home/demobin/epan ntfs default 0 2
/dev/sdb5 /home/demobin/dpan ntfs default 0 2
```

### StartupWMClass
`xprop |grep WM_CLASS`

### desktop快捷方式
`sudo vi /usr/share/applications/navicat.desktop`
lantern.desktop
```
[Desktop Entry]
Name=Lantern
Keywords=lantern;proxy;
Exec=lantern
Icon=/home/demobin/Pictures/lantern_logo.svg
Type=Application
NoDisplay=false
StartupWMClass=
```
navicat.desktop
```
[Desktop Entry]
Name=Navicat
Keywords=navicat;proxy;
Exec=/home/demobin/Downloads/navicat121_premium_en_x64/start_navicat
Icon=/home/demobin/Pictures/navicat.png
Type=Application
NoDisplay=false
StartupWMClass=Navicat.exe
```
postman.desktop
```
[Desktop Entry]
Name=Postman
Keywords=postman;
Exec=/home/demobin/Postman/Postman
Icon=/home/demobin/Pictures/postman.png
Type=Application
NoDisplay=false
StartupWMClass=postman
```

### wifi断联
https://askubuntu.com/questions/1030653/wifi-randomly-disconnected-on-ubuntu-18-04-lts
http://seyferseed.ru/en/life-en/ubuntu-realtek-rtl8723ae-driver-fix-slow-wifi-speed-fix.html#sthash.rsSmI35g.dpbs

### l2tp/ipsec vpn
`sudo apt install network-manager-l2tp network-manager-l2tp-gnome`
添加服务器IP、用户名、密码，只勾选CHAP协议，取消
设置路由172.19.0.0 255.255.0.0 172.19.60.1(这个ip来自tail -f /var/log/syslog连接成功时显示，就是vpn client分配到的ip)

### busybox-initramfs 失败
重启进入安装界面，按esc，按F6，修改最下方启动参数中的quiet为all_generic_ide

### adb
插入前
`lsusb`
```
Bus 002 Device 002: ID 8087:8000 Intel Corp. 
Bus 002 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
Bus 001 Device 002: ID 8087:8008 Intel Corp. 
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
Bus 004 Device 002: ID 174c:07d1 ASMedia Technology Inc. 
Bus 004 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
Bus 003 Device 003: ID 1532:0110 Razer USA, Ltd 
Bus 003 Device 002: ID 1532:004d Razer USA, Ltd 
Bus 003 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
```
`插入后`
```
Bus 002 Device 002: ID 8087:8000 Intel Corp. 
Bus 002 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
Bus 001 Device 002: ID 8087:8008 Intel Corp. 
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
Bus 004 Device 002: ID 174c:07d1 ASMedia Technology Inc. 
Bus 004 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
Bus 003 Device 009: ID 2d95:6007  
Bus 003 Device 003: ID 1532:0110 Razer USA, Ltd 
Bus 003 Device 002: ID 1532:004d Razer USA, Ltd 
Bus 003 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
```
得到idVendor为2d95
`sudo vi /etc/udev/rules.d/51-android.rules`
```
SUBSYSTEM=="usb", ATTR{idVendor}=="2d95", MODE="0666", GROUP="plugdev"
```
`sudo chmod a+r /etc/udev/rules.d/51-android.rules`

无线adb

连接时

`adb tcpip 9999`

拔出后

`adb connect telphone-ip:9999`

# gnome系统恢复主目录中文件夹名字为英文
`export LANG=en_US`

`xdg-user-dirs-gtk-update`
