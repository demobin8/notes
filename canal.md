
### mysql开启binlog

my.conf加入如下配置，并重启mysql

> log-bin必须是路径，另外如果更换了路径，需删除conf目录下的meta.data，否则报错：2020-01-13 19:00:24.266 [destination = test , address = /10.0.0.227:3306 , EventParser] ERROR c.a.o.c.p.inbound.mysql.rds.RdsBinlogEventParserProxy - dump address /10.0.0.227:3306 has an error, retrying. caused by java.io.IOException: Received error packet: errno = 1236, sqlstate = HY000 errmsg = Could not find first log file name in binary log index file

```
log-bin=/opt/mysql/log/mysql-bin.log 
expire-logs-days=14
max-binlog-size=500M
server-id=1
```

### 创建canal用户
```
DROP USER canal
CREATE USER canal IDENTIFIED BY 'canal';
GRANT ALL PRIVILEGES ON qingzhou.* TO 'canal'@'%' IDENTIFIED BY 'canal';
```

### canal server
拉镜像
`docker pull canal/canal-server:v1.1.4`
 
docker 启动

```
docker run -d -it -h 1000 -p 11111:11111 -e canal.auto.scan=false -e canal.destinations=example -e canal.instance.master.address=192.168.31.2:3306 -e canal.instance.dbUsername=canal -e canal.instance.dbPassword=canal -e canal.instance.connectionCharset=UTF-8 -e canal.instance.tsdb.enable=true -e canal.instance.gtidon=false --name=canal-server -m 4096m canal/canal-server:v1.1.4
```

默认destinations=example
```
exception=com.alibaba.otter.canal.server.exception.CanalServerException: destination:test should start first
```

### canal-admin
拉镜像
`docker pull canal/canal-admin:v1.1.4`

docker 启动
```
docker run -d -it -h 1000 -v /opt/canal/data:/home/admin/canal-admin/logs -e server.port=8089 -e canal.adminUser=admin -e canal.adminPasswd=123456 --name=canal-admin -p 8089:8089 -m 1024m canal/canal-admin:v1.1.4
```

canal-server重新启动
```
docker run -d -it -h 1000 -p 11111:11111 -p 11110:11110 -e canal.auto.scan=false -e canal.destinations=example -e canal.instance.master.address=192.168.31.2:3306 -e canal.instance.dbUsername=canal -e canal.instance.dbPassword=canal -e canal.instance.connectionCharset=UTF-8 -e canal.instance.tsdb.enable=true -e canal.instance.gtidon=false -e canal.admin.manager=192.168.31.2:8089 -e canal.admin.port=11110 -e canal.admin.user=admin -e canal.admin.passwd=fe3ab38fa51e360454fff740458b7aa3673596ea --name=canal-server -m 4096m canal/canal-server:v1.1.4
```

异常

`docker run -d -it -h 1000 -p 11111:11111 -p 11110:11110 -p 11112:11112 --name=canal-server -m 4096m canal/canal-server:v1.1.4`

官方支持的是--net=host的方式，现在的方式在服务启动后无法连接到canal-admin，需进入容器命令行，执行如下操作
```
docker exec -it canal-server /bin/sh 
cd canal-server/bin/
sh stop.sh
vi ../conf/canal.properties
```

### 编辑canal.properties，内容如下：

```

#################################################
######### common argument #############
#################################################
# tcp bind ip
canal.ip =
# register ip to zookeeper
canal.register.ip = 10.0.0.227
canal.port = 11111
canal.metrics.pull.port = 11112
# canal instance user/passwd
# canal.user = canal
# canal.passwd = E3619321C1A937C46A0D8BD1DAC39F93B27D4458
# canal admin config
canal.admin.manager = 10.0.0.227:8089
canal.admin.port = 11110
canal.admin.user = admin
canal.admin.passwd = 6BB4837EB74329105EE4568DDA7DC67ED2CA2AD9
canal.zkServers =
# flush data to zk
canal.zookeeper.flush.period = 1000
canal.withoutNetty = false
# tcp, kafka, RocketMQ
canal.serverMode = tcp
# flush meta cursor/parse position to file
canal.file.data.dir = ${canal.conf.dir}
canal.file.flush.period = 1000
## memory store RingBuffer size, should be Math.pow(2,n)
canal.instance.memory.buffer.size = 16384
## memory store RingBuffer used memory unit size , default 1kb
canal.instance.memory.buffer.memunit = 1024
## meory store gets mode used MEMSIZE or ITEMSIZE
canal.instance.memory.batch.mode = MEMSIZE
canal.instance.memory.rawEntry = true
## detecing config
canal.instance.detecting.enable = false
#canal.instance.detecting.sql = insert into retl.xdual values(1,now()) on duplicate key update x=now()
canal.instance.detecting.sql = select 1
canal.instance.detecting.interval.time = 3
canal.instance.detecting.retry.threshold = 3
canal.instance.detecting.heartbeatHaEnable = false
# support maximum transaction size, more than the size of the transaction will be cut into multiple transactions delivery
canal.instance.transaction.size = 1024
# mysql fallback connected to new master should fallback times
canal.instance.fallbackIntervalInSeconds = 60
# network config
canal.instance.network.receiveBufferSize = 16384
canal.instance.network.sendBufferSize = 16384
canal.instance.network.soTimeout = 30
# binlog filter config
canal.instance.filter.druid.ddl = true
canal.instance.filter.query.dcl = false
canal.instance.filter.query.dml = false
canal.instance.filter.query.ddl = false
canal.instance.filter.table.error = false
canal.instance.filter.rows = false
canal.instance.filter.transaction.entry = false
# binlog format/image check
canal.instance.binlog.format = ROW,STATEMENT,MIXED
canal.instance.binlog.image = FULL,MINIMAL,NOBLOB
# binlog ddl isolation
canal.instance.get.ddl.isolation = false
# parallel parser config
canal.instance.parser.parallel = true
## concurrent thread number, default 60% available processors, suggest not to exceed Runtime.getRuntime().availableProcessors()
#canal.instance.parser.parallelThreadSize = 16
## disruptor ringbuffer size, must be power of 2
canal.instance.parser.parallelBufferSize = 256
# table meta tsdb info
canal.instance.tsdb.enable = true
canal.instance.tsdb.dir = ${canal.file.data.dir:../conf}/${canal.instance.destination:}
canal.instance.tsdb.url = jdbc:h2:${canal.instance.tsdb.dir}/h2;CACHE_SIZE=1000;MODE=MYSQL;
canal.instance.tsdb.dbUsername = canal
canal.instance.tsdb.dbPassword = canal
# dump snapshot interval, default 24 hour
canal.instance.tsdb.snapshot.interval = 24
# purge snapshot expire , default 360 hour(15 days)
canal.instance.tsdb.snapshot.expire = 360
# aliyun ak/sk , support rds/mq
canal.aliyun.accessKey =
canal.aliyun.secretKey =
#################################################
######### destinations #############
#################################################
#canal.destinations = example
# conf root dir
canal.conf.dir = ../conf
# auto scan instance dir add/remove and start/stop instance
canal.auto.scan = true
canal.auto.scan.interval = 5
canal.instance.tsdb.spring.xml = classpath:spring/tsdb/h2-tsdb.xml
#canal.instance.tsdb.spring.xml = classpath:spring/tsdb/mysql-tsdb.xml
canal.instance.global.mode = spring
canal.instance.global.lazy = false
canal.instance.global.manager.address = ${canal.admin.manager}
#canal.instance.global.spring.xml = classpath:spring/memory-instance.xml
canal.instance.global.spring.xml = classpath:spring/file-instance.xml
#canal.instance.global.spring.xml = classpath:spring/default-instance.xml
canal.admin.register.auto = true
canal.admin.register.cluster =
```

启动
`sh startup.sh`




