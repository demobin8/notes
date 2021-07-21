[blog](https://xu3352.github.io/linux/2017/05/02/tomcat-cpu-100-utilisation)

`top -H -p [pid]`

```
jps
jstack -J-d64 [pid]
jstack -J-d64 -l [pid-tid]
```

`jstat -gcutil [pid] 1000 5`

### dump head
`jmap -dump:format=b,file=/root/headmap.out [pid]`

### jprofiler

图形化内存分析

### jhat analysis

`jhat -J-Xmx512m headmap.out`

http://127.0.0.1:7000

### hashmap infinite loop


### relic apm
```
eu01xxf3153e4c7eb90a1ceb2ecc110c78420301
```
