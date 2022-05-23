### Send debezium kafka signal
```
./kafka-console-producer --broker-list millitrans-etl-kafka:9092 --topic debezium_signal_dev_etl --property "parse.key=true" --property "key.separator=:"
>     source-connector-etl:{"type":"execute-snapshot","data": {"data-collections": ["etl.menu_items"], "type": "INCREMENTAL"}}
```
### Set kafka topic offset
```
kafka-consumer-groups --bootstrap-server millitrans-el-kafka:9092 --group connect-uat-sink-truck --reset-offsets --to-latest --all-topics --execute
```
### log TRACE
```
curl -s -X PUT -H "Content-Type:application/json" http://localhost:8083/admin/loggers/io.confluent.connect.jdbc.sink -d '{"level": "TRACE"}' | jq
```
