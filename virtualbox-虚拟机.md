> ...

挂载虚拟光驱启动，选择安装到第一个分区，出现

UIDE,01-15-2008 80-MB cache,CD/DVD name is mscd001

IDE1 controller at IO address Fgooh ,chip I.D.1002438ch
IDE2 controller at IO address Fbooh ,chip I.D.10024380h
IDE2 secondary-slave disk is WDC WD 1600AAjs-22psao,ata-133
CD:IDE1 primary-master, teclast DHB16H,ATA-33.
CDROM=1
CDROM1=D:

使用winpe启动，并从ghost安装完成，重启出现

FATAL：INT18：BOOT FAILURE

继续winpe启动，打开PM磁盘工具，右键C盘，修改为主分区，再右键设为活动，完成重启从硬盘启动。

启动发现两边黑框，安装vm增强tools即可。

http://www.gubatron.com/blog/2011/08/29/how-to-resize-a-virtualbox-vdi-fixed-size-virtual-drive-on-mac/
