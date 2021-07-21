> 那时候并不知道自己写一大堆route和iptables配置就是现在所谓的网络即服务

iptables工作在三层，即这是软件过滤，那么若程序跑RAW_SOCKET，它能不能接受到报文呢。

iptables [-t filter] command [match] [target/jump]

          表 命令 匹配的参数  操作

命令：

-A append rules 增加规则

格式：`iptables -A chain rule`

示例：`iptables -A INPUT -j REJECT`

-D delete rules 删除规则  

格式：`iptables -D chain rulenum` （可以用iptables -nL 显示规则的编号）

示例：`iptables -D INPUT 1`

-I insert rules 插入规则

格式：`iptables -I chain rule`

示例：`iptables -I OUTPUT -j DROP`

-L list rules 显示所有规则

格式：iptables -L [chain] [option]

示例：`iptables -nL`

-F delete one by one 加链名删除该链的所有规则

格式：iptables -F [chain]

示例：`iptables -F`

匹配规则：
-p tcp/udp/icmp 指定要匹配的协议 可以加！取反匹配
-s ip 指定匹配源地址的IP
-d ip 指定匹配目的地址的IP

-i 指定要匹配的网络适配器

示例：

`iptables -I FORWARD -p icmp -j REJECT`

`iptables -A INPUT -p tcp -s 192.168.1.100 -j REJECT

`iptables -A INPUT -i eth0`

MAC过滤：

`iptables -A INPUT -m--mac-source xx:xx:xx:xx:xx:xx -j ACCEPT`

 
IPTABLES白表实现示例

`iptables -P INPUT DROP`

应对每一个链都设置，这里省略

`iptables -I INPUT -s 192.168.1.100 -j ACCEPT`

IPTABLES黑表实现示例

`iptables -P INPUT ACCEPT`

应对每一个链都设置，这里省略

`iptables -I INPUT -s 192.168.1.100 -j DROP`

 

子网掩码与广播地址：

192.168.100.22/255.255.255.255

取IP地址的前(255.255.255.255有32个1 )32位有效，即一个子网有1个主机，192.168.100.22/255.255.255.255=192.168.100.22

192.168.100.22/255.255.255.248。写法为192.168.100.22/1

取IP地址的前（255.255.255.248有29个1）29位有效，即一个子网有2的（32-29）次方=8个主机，即分为192.168.100.1-8、192.168.100.8-16。。。等

以此类推，所以192.168.100.22/255.255.255.248是在192.168.100.16-24子网。写法为192.168.100.16/29。
