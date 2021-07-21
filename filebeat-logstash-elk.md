### filebeat start
`sudo ./filebeat -e -c filebeat.yml`

### logstash start
`./bin/logstash -f config/logstash-test.conf`

### filebeat multiline option
```
multiline.pattern: '^SEC_'
multiline.negate: true
multiline.math: after
multiline.flush_pattern: '^\t\t<\/TX>\]'
```

### filebeat output.kafka
```
enable: true
hosts: ['128.196.111.164:9200']
topic: zptestlog
```

### logstash kafka input
```
input {
  kafka {
    bootstrap_servers => ["128.196.111.164:9092"]
    auto_offset_reset => "latest"
    topics => ["zptestlog"]
  }
}
```

### logstash elasticsearch output
```
output {
  elasticsearch {
    hosts => ["localhost:9200"]
    index => "zp"
  }
}
```
