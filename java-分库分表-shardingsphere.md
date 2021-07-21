### pom.xml
```
        <dependency>
            <groupId>org.apache.shardingsphere</groupId>
            <artifactId>sharding-jdbc-spring-boot-starter</artifactId>
            <version>4.1.1</version>
        </dependency>
        <dependency>
            <groupId>org.apache.shardingsphere</groupId>
            <artifactId>sharding-jdbc-spring-namespace</artifactId>
            <version>4.1.1</version>
        </dependency>
```

### config
```
  # db配置
  shardingsphere:
          datasource:
            names:
              master,slave
            # 主数据源
            master:
              type: com.alibaba.druid.pool.DruidDataSource
              driver-class-name: com.mysql.cj.jdbc.Driver
              url: jdbc:mysql://192.168.1.2:3306/test_master?useUnicode=true&characterEncoding=utf-8&serverTimezone=GMT%2b8&nullCatalogMeansCurrent=true
              username: root
              password: 123456
            # 从数据源
            slave:
              type: com.alibaba.druid.pool.DruidDataSource
              driver-class-name: com.mysql.cj.jdbc.Driver
              url: jdbc:mysql://192.168.1.2:3306/test_slave?useUnicode=true&characterEncoding=utf-8&serverTimezone=GMT%2b8&nullCatalogMeansCurrent=true
              username: root
              password: 123456
          props:
            # 开启SQL显示，默认false
            sql:
              show: true
          sharding:
            master-slave-rules:
              ds0:
                master-data-source-name: master
                slave-data-source-names: slave
                load-balance-algorithm-type: round_robin
            tables:
              t_user:
                actual-data-nodes: ds0.t_user${0..1}
                table-strategy.inline.sharding-column: id
                table-strategy.inline.algorithm-expression: t_user${id % 2}
                key-generator.column: id
                key-generator.type: SNOWFLAKE
  datasource:
    druid:
        initialSize: 5
        minIdle: 5
        maxActive: 20
        maxWait: 60000
        timeBetweenEvictionRunsMillis: 60000
        minEvictableIdleTimeMillis: 300000
        validationQuery: SELECT 1 FROM DUAL
        testWhileIdle: true
        testOnBorrow: false
        testOnReturn: false
        poolPreparedStatements: true
        filters: stat,wall
        maxPoolPreparedStatementPerConnectionSize: 20
        useGlobalDataSourceStat: true
        connectionProperties: druid.stat.mergeSql=true;druid.stat.slowSqlMillis=500
```
