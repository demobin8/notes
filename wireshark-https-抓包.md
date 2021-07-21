> windows同理

### SSLKEYLOGFILE
环境变量
```
export SSLKEYLOGFILE='~/ssl.log'
```
并使它生效
`source ~/.bashrc`

### 确认写入
打开chrome(如果没写入就用firefox)打开https://baidu.com
确认ssl.log生成

### 设置wireshark
edit->preferences->protocols-SSL
设置(pre)-Master-Secret log filename为~/ssl.log

### 查看流
同个浏览器重新打开网址，右键跟踪流即可
