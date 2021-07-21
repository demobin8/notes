> 零几年的笔记了，当时写在百度空间，现在百度空间都没了10年了。。。

### 0x01打开命令行的自动补全

vi编辑~/.bahsrc，跳转到最后，将bash_completion相关的几行注释，保存退出。

然后用source ~/.bashrc命令执行~/.bashrc文件使之立即生效，双击tab命令行自动补全，忘记命令或者参数都可以尝试，非常方便。

### 0x02让python的命令行自启动自动补全

vi编辑~/.bashrc

```
PYTHONSTARTUP='/etc/pythonstartup.conf'  #python自启动命令补全配置

export PYTHONSTARTUP
```

vi编辑/etc/pythonstartup.conf

```
try:

    import readline

except ImportError:

    print "readline not avalable"

else:

    import rlcompleter

    readline.parse_and_bind("tab:complete")
```

### 0x03让ls显示更人性化

vi编辑~/.bashrc，添加

alias ll='ls -lh' #设置ls -lh指令的别名为ll

这样每次用ll会更人性化的输出文件大小，比较顺眼。

### 0x04任意目录右键打开终端

`apt-get install nautilus-open-terminal`

### 0x05提高系统音量

`apt-get install alsamixer`

左右键选择标签，上下键调整大小，ctrl+z保存退出，esc取消退出

### 0x06安装flash-player插件播放视频

`apt-get install flashplugin`

### 0x07使用root用户登录

```
sudo passwd root（输入密码）

su root（输入密码）
```

修改如下配置文件
```
vi /etc/lightdm/users.conf
minimum-uid=0
vi /etc/lightdm/lightdm.conf
greeter-hide-users=true 
greeter-show-manual-login=true 

allow-guest=false
```

重启

### 0x08使terminal终端历史缓存无限制

点击终端编辑菜单，选择配置文件首选项，选择滚动标签，勾选不限制即可。清空历史缓存使用命令reset

### 0x09频繁使用的指令使用别名

`alias update='sudo apt update'`

`alias ssh1='ssh -v -l root 192.168.1.2'`

### 0x10区域截图

`shift + prtsc`

### 0x11实时日志

大部分人使用tail

`tail -f test.log`

建议使用less，可以更方便的查找

`less test.log`

`shift + f`

压缩的日志也可以查看（不手动解压）

`zless test.log.gz`

### 0x12硬盘、目录情况查看

影片整体情况

`df -h`

目录下的文件大小

`du -c -h --max-depth=1`

### 0x13文件并集合并

`cat 1.txt 2.txt | sort | uniq > 3.txt`

同理交集和差集分别为`uniq -d`和`uniq -u`

### 0x14查看进程使用的资源

到目录`/proc/[pid]`
```
cat cmdline
cat limits
...
```
