> 十多年过去了，svn也慢慢走出视野淘汰了

### 0x01帮助

`svn help`

`svn help cmd`查看某个操作指令的详细帮助

### 0x02检出

`svn co "url" --username="xxx" --password="xxx"`

### 0x03切换

`svn switch --relocate "url1" "url2"`若svn服务器ip改变要用到

### 0x04提交修改

`svn ci -m "message" xxx.c xxx.h`可以提交所有修改，指定文件或者指定目录

### 0x05更新／更新到指定版本

`svn up`更新到最新

`svn up -r100`更新到指定版本

更新时前面的标志含义如下：

    A  已添加

    D  已删除

    U  已更新

    C  合并冲突

    G  合并成功

    E  已存在

### 0x07添加／删除文件

`svn add／del file`

### 0x08比较差异

`svn diff file`和最新版本比较差异

`svn diff file -r100`和指定版本比较差异

`svn diff file -b`忽略空白数量的修改

### 0x09日志

`svn log` 查看所有日志

`svn log -v`详细日志

`svn log -v -l 100`日志追溯上限以免信息过多

### 0x10添加目录

`svn mkdir`

### 0x11查看状态

`svn st`

可能状态如下：

       “ ” 无修改

      “A” 增加 add

      “C” 冲突 clash

      “D” 删除 delete

      “I” 忽略 ignore

      “M” 改变 modify

      “R” 替换 replace

      “X” 未纳入版本控制的目录，被外部引用的目录所创建

      “?” 未纳入版本控制

      “!” 该项目已遗失(被非 svn 命令删除)或不完整

      “~” 版本控制下的项目与其它类型的项目重名

### 0x12查看版本信息

`svn info`

### 0x13合并分支

`svn merge url1 url2` 这个在更新主线代码的且维护branch时非常有用，使程序员没有忘记同时更新两个地方的烦恼。

### 0x14恢复，即取消修改

`svn revert`
