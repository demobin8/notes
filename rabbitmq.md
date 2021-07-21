
### docker 
启动

`docker run -d --name rabbit -e RABBITMQ_DEFAULT_USER=test -e RABBITMQ_DEFAULT_PASS=123456 -p 15672:15672 -p 5672:5672 -p 25672:25672 -p 61613:61613 -p 1883:1883 rabbitmq:3-management`

docker进入容器

`docker exec -it rabbit bashhelp`

`rabbitmqadmin help subcommandslist`

bindings

`rabbitmqadmin -u test -p 123456 list bindings`

queues

`rabbitmqadmin -u test -p 123456 list queues`

exchanges

`rabbitmqadmin -u test -p 123456 list exchanges`

users

`rabbitmqadmin -u test -p 123456 list users`

connections

`rabbitmqadmin -u test -p 123456 list connections`

channels

```
rabbitmqadmin -u test -p 123456 list channelspublish
rabbitmqadmin -u test -p 123456 publish routing_key=order_status_binding_key exchange=normalOrderStatusExchange payload="aaaaaaaaaaaaaaaaaaaaaaaa"get
rabbitmqadmin -u test -p 123456 get queue=normalOrderStatusQueue
```

多条

`rabbitmqadmin -u test -p 123456 get queue=normalOrderStatusQueue count=10`

不进行requeue，就是消费完删掉
```
rabbitmqadmin -u test -p 123456 get queue=normalOrderStatusQueue count=1 ackmode=ack_requeue_falsedeclare
rabbitmqadmin -u test -p 123456 declare queue name=testQueue
rabbitmqadmin -u test -p 123456 declare exchange name=testExchange type=topic
rabbitmqadmin -u test -p 123456 declare binding source=testExchange destination=testQueue routing_key=testQueuedelete
rabbitmqadmin -u test -p 123456 delete binding source=testExchange destination=testQueue destination_type=queue
```

### windows shell
```
PS C:\Users\demobin> rabbitmqctl.bat list_users
Listing users ...
user    tags
guest   [administrator]
PS C:\Users\demobin> rabbitmqctl.bat add_user test test123#
Adding user "test" ...
PS C:\Users\demobin> rabbitmqctl.bat list_users
Listing users ...
user    tags
test []
guest   [administrator]
PS C:\Users\demobin> rabbitmqctl.bat set_user_tags test administrator
Setting tags for user "test" to [administrator] ...
PS C:\Users\demobin> rabbitmqctl.bat list_users
Listing users ...
user    tags
test [administrator]
guest   [administrator]
PS C:\Users\demobin> rabbitmqctl.bat set_permissions -p / test '.*' '.*' '.*'
Setting permissions for user "test" in vhost "/" ...
```

