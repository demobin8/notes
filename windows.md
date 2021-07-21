### 端口占用
```
netstat -aon|findstr "9999"

TCP    0.0.0.0:9999           0.0.0.0:0              LISTENING       24224
TCP    [::]:9999              [::]:0                 LISTENING       24224
tasklist|findstr "24224"

java.exe                     24224 Console                    2    240,024 K
taskkill /f /pid 24224
```

* 杀死进程需要管理员权限运行cmd

> 成功: 已终止 PID 为 24224 的进程。

### Ctrl + Shift + F热键冲突

关闭繁简体热键，右键微软自带的那个输入法图标，就是那个中，设置，按键，拉到最下有关闭这个热键。

### 开启剪切板记录

设置->剪切板设置->开启

`win + v`查看剪切板

### 指令

```
calc - 计算器

cmd - cmd

notepad - 记事本

mspaint - 画图

regedit - 注册表

gpedit.msc -- 组策略

explorer c: -- 打开文件浏览器并指定位置

devmgmt.msc -- 打开设备管理器

services.msc -- 打开服务

msconfig - 配置、启动

mstc - 远程桌面

nslookup - 域名解析

taskmgr - 任务管理器

```
