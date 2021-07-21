
### client
redis-desktop-manager

### redis与数据库一致性

	* 延时双删策略 - 1、删除缓存 2、写数据库 3、休眠一定时间 4、再次删除缓存
	* 缓存超时 - 超时越短，一致性越高，但数据库压力越大
	* 异步更新缓存 - 读缓存、 写sql、 通过消息订阅mysql的binlog更新缓存

### server
```
./redis-server ./redis.confconf
...
requirepass xiaobin
...
```

### cli
```
./redis-cli -h 127.0.0.1 -p 6379 -a xiaobin
SLOWLOG GET 10
KEYS *
SET demobin handsome
GET demobin
FLUSHALL
```

### redis config
```
config get *
config set timeout 10SET NX PX
NX 只有KEY不存在才设置值
EX 过期时间 秒级
PX 过期时间 毫秒级
```

### GEO
```
GEOADD
GEOADD cityGeo 116.405285 39.904989 "北京"
GEOADD cityGeo 121.472644 31.231706 "上海"
GEOPOS
GEOPOS cityGeo 北京GEODIST
GEODIST cityGeo 北京 上海 kmGEORADIUS
GEORADIUS cityGeo 116.405285 39.904989 100 km WITHDIST WITHCOORD ASC COUNT 5GEORADIUSBYMEMBER
GEORADIUSBYMEMBER cityGeo 北京 100 km WITHDIST WITHCOORD ASC COUNT 5GEOHASH
GEOHASH cityGeo 北京
```

### 自增 原子操作
```
INCR KEY
```

### 分布式锁
redisson
```
        String key = "payment:create:" + dto.getBizOrderCode();
        try {
            if (RedissonLockUtil.tryLock(key, RedissonLockUtil.LOCK_WAIT_TIME, RedissonLockUtil.LOCK_LEASE_TIME)) {
                doPayment(dto);
            }
        } catch (ServiceException e) {
            throw e;
        } catch (Exception e) {
            log.error("==>redisson获取锁异常，异常信息为：{}", e.getMessage());
        } finally {
            RedissonLockUtil.unlock(key);
        }
```

#### 排行榜--STRING
```
ZADD
ZADD key [NX|XX] [CH] [INCR] score member [score member...]ZSCORE
ZSOCRE key memberZREVRANGE
ZREVRANGE key start stop [WITHSCORES]ZREVRANK 
ZREVRANK key memberZINCRBY
ZINCRBY key increment memberZREM
ZREM key memberDEL
DEL key
```

### 统计--BITMAP
```
SETBIT
SETBIT key offset valueGETBIT
GETBIT key offset点赞SADD
SADD key member [member...]SREM
SREM key member [member...]SISMEMBER
SISMEMBER key member
```

### 分页排序--ZSET
```
ZADD
```

### 购物车--HASH
```
HSET
HSET key field valueHEXIST
HEXISTS key field
```

### 附近的X-GEOGEOADD
```
GEOADD key longitude latitude memberGEODIST
GEODIST key member1 member2 [m|km|ft|mi]GEORADIUS
GEORADIUS key longitude latitude radius m|km|ft|mi [WITHCOORD] [WITHDIST] [WITHHASH] [COUNT count] [ASC|DESC] [STORE key] [STOREDIST key]
```
