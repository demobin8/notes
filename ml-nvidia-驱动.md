> 15年的时候，深度学习还没那么火，nvidia驱动可麻烦了。。。现在生态应该是好多了，都很方便

# CentOS 7 - NVIDIA GTX960驱动安装
笔记本不能使用该方案，b
* [官网](http://www.geforce.cn/drivers) 根据型号查找驱动并下载。
启动参数添加 nomodeset
* 停用nouveav驱动
`/usr/lib/modedprob.d/dist-blacklist.conf`

添加blacklist nouveau

`options nouveau modeset=0`

注释blacklist nvidiafb

`sudo mv /boot/initramfs-$(uname -r).img /boot/initramfs-$(uname -r).img.bak`

`sudo dracut -v /boot/initramfs-$(uname -r).img $(uname -r)`

修改/etc/inittab，使重启只进入文本模式，查看inittab文件可知，inittab已经被systemd取代，文本模式和图形模式切换方法如下：
```
mv /etc/systemd/system/default.target /etc/systemd/system/default.target.bak         (改名备份)
ln -sf /lib/systemd/system/multi-user.target /etc/systemd/system/default.target      (重新软连接文本界面为启动默认值界面)
reboot                                                                               (重启)

恢复图形界面

rm -rf  /etc/systemd/system/default.target                                          (移除当前配置链接)
mv  /etc/systemd/system/default.target.bak /etc/systemd/system/default.target       (恢复备份配置链接)
reboot        
```
重启
* 安装驱动
```
chmox +x /path/to/your/nvidia-driver.run
sh /path/to/your/nvidia-driver.run
reboot
```
* 修改分辨率
`vi /etc/X11/xorg.conf`

将

```
 HorizSync 28.0 - 33.0
 VertRefresh 43.0 - 72.0
 ```
 
修改

```
 HorizSync 30.0 - 83.0
 VertRefresh 56.0 - 75.0
```
