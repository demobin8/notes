
### docker安装启动postgres:9.6--高版本会报错
`docker run -d --name kong-database -p 5432:5432 -e "POSTGRES_USER=kong" -e "POSTGRES_DB=kong" -e "POSTGRES_PASSWORD=kong" postgres:9.6`

### helm安装启动kong
`helm install kong stable/kong --set=env.database=postgres,postgres.enabled=true,env.pg_host=192.168.31.2,env.pg_port=5432,env.pg_user=kong,env.pg_database=kong`

### docker初始化konga数据库
`docker run --rm pantsel/konga:latest -c prepare -a postgres -u postgresql://kong:@192.168.31.2:5432/konga`

### docker启动konga--主要设置了node通过ssl自签名证书
`docker run -p 1337:1337 -e "DB_ADAPTER=postgres" -e "DB_HOST=192.168.31.2" -e "DB_PORT=5432" -e "DB_USER=kong" -e "DB_DATABASE=konga" -e "NODE_ENV=production" -e "NODE_TLS_REJECT_UNAUTHORIZED=0" --name konga pantsel/konga`

### 查看kong-kong-admin端口
`kubectl get svc`
登录注册使用

### 跨域设置
由于kong在面对复杂跨域请求(preflight 预检请求 json 格式触发)时有问题，所以如果后端springboot有支持跨域，直接开启kong的cors插件的preflight-continue即可，不用设置其他参数，无效

### service连接不上问题追踪
查看pod，登录pod检查本地服务开启，检查kube-proxy服务是否正常

### 部署不成功的问题追踪
登录kong wait-for-db pod，手动执行数据库迁移脚本

### kong websocket
注意路径
