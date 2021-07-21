### 统计响应超过1秒的接口

`grep -E '([1-9]{4} ms)' *.log | awk '{print $3}' | sort | uniq -c |sort -nr`

### 按行合并两个文件

`paste -d ':' a b`

### ping with date

`ping 172.16.6.162 | while read line; do echo `date` - $line; done`

### reset tcp connection

`ss -K dst 192.168.1.214 dport = 49029`

### htop

按大写的M以内存占用排序，P以CPU占用排序，T以时长排序，按I倒转排序

按t以树形结构展示

按k给选中的进程发信号

按u展示特定用户的进程

按/搜索进程

### iftop 

按大写的D切换展示目标端口信息，按小写p切换展示源端口信息

按P暂停

按b显示平均流量图形条，按B切换平均流量的统计时间10，20，40秒

按j/k上下滚动

按<以源主机排序，>以目标主机排序

bash

### 指令回显

`set -x`

`+cp a b`


### 只拷贝目录，只拷贝一级目录下的指定文件

`find jobs -type d | sed 's/jobs/mkdir -p myjobs/' | sh`

`find jobs -maxdepth 1 -type d | sed 's/jobs/mkdir -p myjobs/' | sh`

`find jobs -maxdepth 2 -name config.xml | sed 'p; s/jobs/myjobs/' | sed 'N; s/\n/ /' | sed 's/^/cp /' | sh`


### 修改指定文件的所有特定文本

`find . -name config.xml -exec sed -i 's/home/demo/' {} \;`


### 打开ip_forward

```
/etc/sysctl.conf
net.ipv4.ip_forward = 1
```

### 修改提示符linux /etc/profile

```
export PS1="[\u@\h:`pwd`]\$"
```

### 排序sort

`sort -t ':' -k 1 bigram.txt -o bigram.rst`

`sort -n -r -k 2 -t $'\t ' news-charcnt.txt`

### 唯一uniq

`uniq -c`

### 统计awk sum

`ls | xargs cat | awk -F '\t' '{arr[$1]+=$3;} END {for (i in arr) print i, arr[i]}' >> ../sum.txt`

### 重命名rename

`rename 's/$/.txt/' *.py`

### 中文乱码convmv

```
find . | iconv -f gb18030 -t utf-8
convmv -r -f gb18030 -t utf-8 --notest .
```

### 查找执行find

`find . -name "*.txt" -exec mv -t ../3/ {} \;`

`find . -name "*.py" -exec cat {} \; | wc -l`

`find . -name "*.java" -exec grep -nr ' do' {} -H \;`

### wget

输出到终端

`wget http://127.0.0.1:8080/api/snowflake/get/test -q -O -`

`wget https://127.0.0.1:8444/upstreams --no-check-certificate -q -O -`

### 匹配sed

`I -- case insensitive`
`d -- delete`
`-i -- edit in the file`
`regex match like vim search`

### sed 非贪婪

`sed -i 's/^app.loginUrl=http:\/\/[^/]*\/\(.*\)/app.loginUrl=http:\/\/'$DEFAULT_APP_ADDR'\/\1/g' $CONFIG_PATH/$APP_FILENAME`

`sed -i.bak '/\(wＷw．xiＡoshＵotxt.cＯm\|www.xiaoshuotxt.,com\)/Id' ./ebook.txt`

### grep

`grep -vE 'old|new' convmv.sh`

### 显示匹配的行的上下文的行

`grep -r -C2 'selector' .`

### sshfs

`sshfs -o server root@192.168.88.3:/mnt/user/stephen`

### dd

`sudo dd if=xxx.iso of=/dev/sdb bs=1M`

### 分割文件split

`split -l 20480000 news.seg.2gram.sorted.preprocessed split`

### 并行执行指令parallel

`ls | parallel -m -j 8 "cat {} >> ../news.txt"`

> 参考：http://randyzwitch.com/gnu-parallel-medium-data/

### 复制命令行输出xclip

`ls | xclip`

`cat words.txt | xclip`

### 截图gnome-screenshort

`gnome-screenshort -a`

### ubuntu shortcuts

`shift+print screen`

### sshfs

`sshfs -o server root@192.168.88.3:/root/`

### unzip指定编码

防止windows压缩文件在linux下解压目录文件乱码

`unzip -O cp936 test.zip`

### watch

`watch -n1 nvidia-smi`

### 保存到数组

```
src=($(cat s.list))
dst=($(cat d.list))
for i in {0..100}
do
  echo ${src[$i]} ${dst[$i]}
done
```
### 把目录下的所有类型指定文件拷贝到指定目录

1. Find all files without directory with test

`find . -name "*.h"  -not -path "*test*" > files.sh`

2. Create cp bash with vim cmd

`vim -c "g/^.\(.*\)\/\(.*\)/s//cp .\1\/\2 \/dir\/webrtc\/modules\1/g | q" files.sh`
>`vim -c "his | q"` to check vim history

3. Mkdirs

`cat files.sh | awk '{print $3}' | sort -u | xargs mkdir -p`

4. Excute files.sh

`bash files.sh`

或者使用脚本
```
for file in $(find . -type f -name '*.h')
do
    mkdir -p "dir/$(dirname $file)"
    cp $file "dir/$file"
done
```
### ssh-keygen
`ssh-keygen -t rsa -C "demobin@163.com"`

### 快速返回刚才的目录
`cd -`

### 快速进入主目录
`cd`

### 快速执行历史命令
输入!感叹号加history的id回车
`history`
```
 1433  git status
 1434  git pull
 1435  git pull origin main
 1436  ll
 1437  ll | wc -l
```
`!1435`

### vim普通用户打开的文件编辑后保存
避免改了半天却因无法保存而丢失改动的情况
`:w !sudo tee %`
完成之后，`:q!`强制退出即可

### 快速清空（存在）或创建一个文件
`> test.py`
