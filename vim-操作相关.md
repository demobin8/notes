### Lazy Matching
```
-. greedy
.*
-. lazy
.\{-}
```

### Merge
```
-. v mode
ggvGJ
-. cmd mode
:1, 20j
```

### Serial Number
```
let i=0 | g/^/s//\=i/ | let i=i+1
```

### Case No Sensitive
```
/regex\c
```

### Fast Word Search
```
#
```

### Calculate Match Sentence
```
s/(void \*)(p + \(\d\+\))/\='p->cn.a'.(submatch(1)-32)/g
```

### Search lines that not matching the regex
```
:v/regex/
```

### Multi lines search
```
/bottom.*\n.*bottom
```

## 下面是之前记录在百度空间的基础操作，部分快捷键依赖vimrc配置

### 0x01如何快速复制与粘帖？

跳转到文件顶部／尾部：

`gg／G`

粘帖：

`p`

撤销／重做：

`u／ctrl+r`

删除／复制当前行：

`dd／yy`

删除／复制指定多行：

`n1,n2d／y`

或者更方便的删除／复制：

可视模式选择选择删除／复制的内容按

`d／y`

### 0x02如何从系统剪切办复制粘帖？

复制到剪切板：`F4`

从剪切板粘帖：输入模式ctrl+insert，或者右键粘帖

### 0x03如何快速的在两个文件中复制粘帖？

复制粘帖整个文件：

`:r!cat file_to_copy`

复制粘帖另一个文件的前后n行，或者包含指定字符串的行：

`:r!more file_to_copy，:r!tail file_to_copy，:r!grep "string" file_to_copy`

复制粘帖任意位置：

当前文件中复制，再:e命令打开第二个文件粘帖

### 0x04如何插入／删除一列？

插入一列：

可视模式选择一列，按大写I，输入插入的字符，按esc

删除一列：

可视模式选择一列，按d

### 0x05如何查找、替换？

/string_to_search，vim会高亮显示，按n查找下一个，按大写N查找前一个

只替换当前行string：

`:s/string/string_new`

替换当前行所有的string：

`:s/string/string_new/g`

替换指定区域的string：

`:n1,n2s/string/string_new`

或者更方便的，可视模式选择指定区域:

`:s/string/string_new`

替换整个文件的string：

`:g/string/s//string_new/g`

### 0x06如何快速插入当前时间／当前路径／目录文件名／系统版本等信息？

`:r!date，pwd，ls，cat /proc/version`

### 0x07如何类似ultraedit的方式查看文件？

`:%!xxd`

### 0x08如何自动对齐，同时缩进多行？

全文自动对齐：

`F3`

任意缩进多行：

可视模式选择要右／左缩进的行，按>／<

### 0x09如何打开／关闭左侧目录树？

`F5`

### 0x10如何创建TAGS／CSCOPE？

```
ctags -R *

cscope -Rbq
```

### 0x11如何跳转／返回到定义或者声明？

定义跳转：

`ctrl+]`

返回：

`ctrl+t`

### 0x12如何查找并跳转到某变量的赋值语句？

ctrl+\+s查找出该变量所有的赋值语句，按提示前方的number即可跳转
