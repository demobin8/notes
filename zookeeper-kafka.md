### zookeeper

建议副本数3+
> 当部分zookeeper宕机之后，剩下的个数必须大于宕掉的个数，zookeeper才可以继续使用
> 奇数时以最大容错服务器个数的条件下，更节省资源

split-brain

-. Quorums
-. Redundant communications
-. Fencing

zxid溢出
zk会重新选举，选举期间相当于restart，服务不可用

传输数据大小限制
zoo.conf
```
jute.maxbuffer=0x9fffff
```
或者zkServer.sh
```
JVMFLAGS="$JVMFLAGS -Djute.maxbuffer=5000000"
```

### kafka
start

`./bin/kafka-server-start.sh config/server.properties`

kafka server.properties

`listeners=PLAINTEXT://128.196.111.164:9092`

create topic

`./bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test`

delete topic

`./bin/kafka-topics.sh --zookeeper localhost:2181 --delete --topic test`

list topic

`./bin/kafka-topics.sh --list --zookeeper localhost:2181`

describe topic

`./bin/kafka-topics.sh --describe --zookeeper localhost:2181 --topic test`

start producer

`./bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test`

start consumer

`./bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test --from-beginning`

start zookeeper

`./bin/zkServer.sh start ./conf/zoo.cfg`


