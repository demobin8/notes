### 修改docker默认ip段
/etc/docker/daemon.json
```
{
    "default-address-pools": 
        [{
            "base":"10.0.0.1/16","size":24
        }]
}
```

### linux安装
```
yum install docker-ce
yum install -y yum-utils device-mapper-persistent-data lvm2
yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
yum install docker-ce
usermod -aG docker $(whoami)
systemctl enable docker.service
systemctl start docker.serviceyum install docker-compose
yum install epel-release
yum install -y python-pip
pip install docker-compose
yum upgrade python*
docker-compose version
sudo groupadd docker
sudo usermod -aG docker $USER
systemctl enable docker
systemctl start docker
docker run hello-world
```

### 拷贝结束后先

`rm -rf /var/lib/docker/network/files/local-kv.db`

### 重启
```
service docker restart
docker ps
docker network ls
docker rm xxx
```

### docker-compose
```
docker-compose down
docker-compose up -d
```

### 指令

搜索仓库

`docker search redis`

下载镜像

`docker pull redis`

查看所有镜像

`docker images`

删除镜像
`docker rmi pingcap/tidb`

查看所有容器

`docker ps -a`

执行容器指令

`docker exec -it [CONTAINER ID] redis-cli -h localhost -p 6379`

获取镜像元数据

`docker inspect redis`

启动镜像redis

`docker run -d -p 6379:6379 redis --requirepass "ecp"`

停止容器

`docker stop [CONTAINER ID]`

mysql
```
docker run -p 3306:3306 -e MYSQL_ROOT_PASSWORD=xiaobin -v test:/var/lib/mysql -d mysql:latest
mysql -h 0.0.0.0 -uroot -pxiaobin
```

执行指令
`docker exec [CONTAINER ID] bash -c "ls /"`

删除所有退出的容器

`docker rm $(docker ps -a -q)`

删除所有none的镜像

`docker images |grep none | awk -F ' ' '{print $3}' | xargs docker rmi`

查看信息

`docker info`

根据系统进程pid查看容器id和镜像名称

`docker inspect -f '{{.State.Pid}} {{.Id}} {{.Config.Hostname}}' $(docker ps -aq) | grep 7734使用镜像拉取镜像`

其它
```
docker pull docker.mirrors.ustc.edu.cn/library/postgres:latest
postgres
docker run -p 5432:5432 -e POSTGRES_PASSWORD=xiaobin -v /home/demobin/test/pg_hba.conf:/var/lib/postgresql/data/pg_hba.conf -d postgres:latest
psql -h 0.0.0.0 -p 5432 -U postgres提交修改
docker login --username=zengxiaobin510@sina.com registry.cn-hangzhou.aliyuncs.com
docker commit 1cdf73db5fc7 registry.cn-hangzhou.aliyuncs.com/demobin/kali:v1
docker push registry.cn-hangzhou.aliyuncs.com/demobin/kali:v1拷贝文件
docker cp ~/Desktop/bistoury-2.0.6-quick-start.tar.gz b3567aa5dbd7:/root/语言
apt-get install -y locales locales-all
locale -a
env LC_ALL zh_CN.utf8
export LC_ALL=zh_CN.utf8
export LANG=zh_CN.utf8
export LANGUAGE=zh_CN.utf8


docker nacos
docker pull nacos/nacos-server
docker run --env MODE=standalone --name nacos -d -p 9002:8848 nacos/nacos-server
docker kali
docker run -it --name kali registry.cn-hangzhou.aliyuncs.com/demobin/kali:v1
docker stripe-cli
docker run --rm -it stripe/stripe-cli
docker rabbitmq

docker run -d --name rabbit -e RABBITMQ_DEFAULT_USER=vvnotifyservice -e RABBITMQ_DEFAULT_PASS=123456 -p 15672:15672 -p 5672:5672 -p 25672:25672 -p 61613:61613 -p 1883:1883
rabbitmq:3-management
docker tomcat
docker run -d -p 8080:8080  --name tomcat tomcat:latest
docker nginx
docker run -d -p 8080:80 --name nginx -v //c/Users/demobin/webapps:/usr/share/nginx/html nginx
换root，开启目录索引功能

user  root;
worker_processes  1;
error_log  /var/log/nginx/error.log warn;
pid        /var/run/nginx.pid;
events {
    worker_connections  1024;
}
http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;
    autoindex on;
    autoindex_localtime on;
    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';
    access_log  /var/log/nginx/access.log  main;
    sendfile        on;
    #tcp_nopush     on;
    keepalive_timeout  65;
    #gzip  on;
    include /etc/nginx/conf.d/*.conf;
}
```
