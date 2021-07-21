# python的shell环境tab补全
## 1.编辑文件~/.pythonstartup
```
# python startup file
import sys
import readline
import rlcompleter
import atexit
import os

# tab completion
readline.parse_and_bind('tab: complete')
# history file
histfile = os.path.join(os.environ['HOME'], '.pythonhistory')
try:
    readline.read_history_file(histfile)
except IOError:
    pass
atexit.register(readline.write_history_file, histfile)


del os, histfile, readline, rlcompleter 
```

## 2.在/etc/profile添加
`export PYTHONSTARTUP=~/.pythonstartup`

## 3.安装readline
```
yum install readline*
pip install readline
```
## 完成，查看
最后`source一下/etc/profile`使生效即可。
