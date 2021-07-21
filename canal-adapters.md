### 官网

https://github.com/alibaba/canal/wiki/ClientAdapter
https://github.com/alibaba/canal/wiki/Sync-ES

### fix
https://www.jianshu.com/p/96cd1bad5f71

### app
adapter/conf/application.yaml
```
server:
  port: 8081
spring:
  application:
    name: canaladapter-order
  jackson:
    date-format: yyyy-MM-dd HH:mm:ss
    time-zone: GMT+8
    default-property-inclusion: non_null

management:
  metrics:
    export:
      prometheus:
        pushgateway:
          base-url: 127.0.0.1:9091
          enabled: true
          push-rate: 15s
  endpoints:
    web:
      exposure:
        include: 'loggers,metrics'

canal.conf:
  mode: kafka # kafka rocketMQ
#  canalServerHost: 127.0.0.1:11111
#  zookeeperHosts: slave1:2181
  mqServers: 192.168.1.2:9092 #or rocketmq
#  flatMessage: true
  batchSize: 30
  syncBatchSize: 500
  retries: 0
  requestTimeout: 120000
  sessionTimeout: 90000
  timeout:
  accessKey:
  secretKey:
  srcDataSources:
    defaultDS:
      url: jdbc:mysql://127.0.0.1:3306/order?useUnicode=true&characterEncoding=utf-8&serverTimezone=GMT%2b8
      username: root
      password: 123456
  canalAdapters:
  - instance: order_es_business_topic # canal instance Name or mq topic name
    groups:
    - groupId: g1
      outerAdapters:
      - name: logger
#      - name: rdb
#        key: mysql1
#        properties:
#          jdbc.driverClassName: com.mysql.jdbc.Driver
#          jdbc.url: jdbc:mysql://127.0.0.1:3306/mytest2?useUnicode=true
#          jdbc.username: root
#          jdbc.password: 121212
#      - name: rdb
#        key: oracle1
#        properties:
#          jdbc.driverClassName: oracle.jdbc.OracleDriver
#          jdbc.url: jdbc:oracle:thin:@localhost:49161:XE
#          jdbc.username: mytest
#          jdbc.password: 121212
#      - name: rdb
#        key: postgres1
#        properties:
#          jdbc.driverClassName: org.postgresql.Driver
#          jdbc.url: jdbc:postgresql://localhost:5432/postgres
#          jdbc.username: postgres
#          jdbc.password: 121212
#          threads: 1
#          commitSize: 3000
#      - name: hbase
#        properties:
#          hbase.zookeeper.quorum: 127.0.0.1
#          hbase.zookeeper.property.clientPort: 2181
#          zookeeper.znode.parent: /hbase
      - name: es
        hosts: 192.168.1.3:9200 # 127.0.0.1:9200 for rest mode
        properties:
          mode: rest # or rest
          # security.auth: test:123456 #  only used for rest mode
          cluster.name: search-service
```

### es

adapter/conf/es/biz.yml
```
dataSourceKey: defaultDS
destination: example
groupId: g1
esMapping:
  _index: customer
  _type: _doc
  _id: _id
  relations:
    customer_order:
      name: order
      parent: customer_id
  sql: "select concat('oid_', t.id) as _id,
        t.customer_id,
        t.id as order_id,
        t.serial_code as order_serial,
        t.c_time as order_time
        from biz_order t"
  skips:
    - customer_id
  etlCondition: "where t.c_time>={}"
  commitBatch: 3000
```

### rdb
```
dataSourceKey: defaultDS
destination: order_data1
groupId: g1
outerAdapterKey: mysql1
concurrent: true
dbMapping:
  database: order_test
  table: order_details
  targetTable: order_details
  targetPk:
    id: id
  mapAll: true
#  targetColumns:
#  #  #    id:
#  #  #    name:
#  #  #    role_id:
#  #  #    c_time:
#  #  #    test1:
#  #    etlCondition: "where c_time>={}"
  commitBatch: 3000 # 批量提交的大小
```

### 启动
adapter/bin/start.sh

### rdb测试
1. Navicat同步，将源表复制至目标库
2. 启动adapter，
3. 修改源表任意字段值，校验目标库是否同步成功(fix后ddl语句也可同步成功)

### es测试

kibana es建模后，先调用adapter全量同步接口

`curl http://127.0.0.1:8083/etl/es/abcdef.yml -X POST`

随后修改源表任意字段值，校验ES库索引是否同步成功
