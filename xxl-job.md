### docker
`docker pull xuxueli/xxl-job-admin:2.1.1`

### 导入数据库
https://raw.githubusercontent.com/xuxueli/xxl-job/master/doc/db/tables_xxl_job.sql

### 启动
```
docker run -e PARAMS="--spring.datasource.url=jdbc:mysql://192.168.1.2:3306/xxl_job?Unicode=true&characterEncoding=UTF-8 --spring.datasource.username=qingzhou --spring.datasource.password=wwzl2025" -p 19527:8080 -v /opt/xxl-job:/data/applogs --name xxl-job-admin  -d xuxueli/xxl-job-admin:2.1.1
```

### 创建执行器
![image](https://user-images.githubusercontent.com/16394555/124580868-23583f00-de83-11eb-862f-c74f820ea2ce.png)

### 创建任务
![image](https://user-images.githubusercontent.com/16394555/124581073-58649180-de83-11eb-9663-e2bd789eb215.png)

### maven依赖
```
<dependency>
    <groupId>com.xuxueli</groupId>
    <artifactId>xxl-job-core</artifactId>
    <version>${xxl.version}</version>
</dependency>
```

### application.yml配置
```
xxl: 
  job:
    accessToken: ''
    adminAddresses: http://127.0.0.1:7116/xxl-job-admin
    executorAppName: payment-settlement-executor
    executorIp: 
    executorPort: 9906
    executorLogPath: /home/project/payment-settlement-executor/log/
    executorLogRetentionDays: 30
    schema: http:// 
```

### java config
```
@Bean
public XxlJobSpringExecutor xxlJobExecutor() {
    logger.info(">>>>>>>>>>> xxl-job config init.");
    XxlJobSpringExecutor xxlJobSpringExecutor = new XxlJobSpringExecutor();
    xxlJobSpringExecutor.setAdminAddresses(adminAddresses);
    xxlJobSpringExecutor.setAppname(appname);
    xxlJobSpringExecutor.setIp(ip);
    xxlJobSpringExecutor.setPort(port);
    xxlJobSpringExecutor.setAccessToken(accessToken);
    xxlJobSpringExecutor.setLogPath(logPath);
    xxlJobSpringExecutor.setLogRetentionDays(logRetentionDays);
    return xxlJobSpringExecutor;
}
```

### java executor
```
    @XxlJob("settlement")
    public ReturnT<String> execute(String param) {
        jobService.settlement();
        return ReturnT.SUCCESS;
    }
```

### 无法自动注册
项目代码配置的appName必须与执行器的appName一致
