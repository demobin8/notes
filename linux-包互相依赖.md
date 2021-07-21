> 现在的发行版似乎很少遇到这种问题了

deb文件下载官网packages.ubuntu.com，apt用代理时最好直接在网址上下载比较快

查看所有已安装的软件包`dpkg -l`，(配合grep使用比较好)

查看包个软件包的依赖性`apt-cache depends xxx`

强制安装（还可以加--force，不过我没有加也行）

`dpkg -i a.deb`

`dpkg -i b.deb`

修复依赖关系

`dpkg --configure -a`
