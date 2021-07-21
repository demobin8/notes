### forwarding
`ssh -gfnNTR xxx.xxx.xxx.xxx:7001:127.0.0.1:22 root@xxx.xxx.xxx.xxx -o ServerAliveInterval=30 -p 6000`

### bash
```
#!/bin/bash
rst=`ps -ef|grep "ssh -gfnNTR"|awk '{print $8}'`
if [ "$rst" == "grep" ]; then
    sshpass -p 'xxx' ssh -gfnNTR xxx.xxx.xxx.xxx:7001:127.0.0.1:22 root@xx.xxx.xxx.xxx -o ServerAliveInterval=30 -p 6000
fi
```

### crontab
`0 */1 * * * /home/demobin/home.sh`

### tunnel
`ssh -NfL 9528:10.0.0.24:9527 root@xxx.xxx.xxx.xxx -p 2222`

