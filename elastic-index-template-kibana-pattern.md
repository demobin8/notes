### log context
```
{
  "index_patterns": ["context-log-*"],
  "priority": 1,
  "template": {
    "settings": {
      "number_of_shards": "${NUMBER_OF_SHARDS}",
      "refresh_interval": "${REFRESH_INTERVAL}"
    },
    "mappings": {
      "dynamic_templates": [
        {
          "context": {
            "path_match": "context.*",
            "match_mapping_type": "string",
            "mapping": {
              "type": "keyword"
            }
          }
        },
        {
          "stats": {
            "path_match": "stats.*",
            "mapping": {
              "type": "scaled_float",
              "scaling_factor": 1000
            }
          }
        },
        {
          "perf_stats.count": {
            "path_match": "perf_stats.*.count",
            "mapping": {
              "type": "integer"
            }
          }
        },
        {
          "perf_stats.total_elapsed": {
            "path_match": "perf_stats.*.total_elapsed",
            "mapping": {
              "type": "long"
            }
          }
        },
        {
          "perf_stats.read_entries": {
            "path_match": "perf_stats.*.read_entries",
            "mapping": {
              "type": "integer"
            }
          }
        },
        {
          "perf_stats.write_entries": {
            "path_match": "perf_stats.*.write_entries",
            "mapping": {
              "type": "integer"
            }
          }
        }
      ],
      "properties": {
        "@timestamp": {
          "type": "date",
          "format": "strict_date_optional_time"
        },
        "id": {
          "type": "keyword"
        },
        "app": {
          "type": "keyword"
        },
        "host": {
          "type": "keyword"
        },
        "result": {
          "type": "keyword"
        },
        "correlation_id": {
          "type": "keyword"
        },
        "ref_id": {
          "type": "keyword"
        },
        "client": {
          "type": "keyword"
        },
        "action": {
          "type": "keyword"
        },
        "error_code": {
          "type": "keyword"
        },
        "error_message": {
          "type": "text",
          "index": "false"
        },
        "elapsed": {
          "type": "long"
        }
      }
    }
  }
}

```
### trace 
```
{
  "index_patterns": ["trace-*"],
  "priority": 1,
  "template": {
    "settings": {
      "number_of_shards": "${NUMBER_OF_SHARDS}",
      "refresh_interval": "${REFRESH_INTERVAL}"
    },
    "mappings": {
      "properties": {
        "@timestamp": {
          "type": "date",
          "format": "strict_date_optional_time"
        },
        "app": {
          "type": "keyword"
        },
        "result": {
          "type": "keyword"
        },
        "action": {
          "type": "keyword"
        },
        "error_code": {
          "type": "keyword"
        },
        "content": {
          "type": "text",
          "index": "false"
        }
      }
    }
  }
}
```
### stat
```
{
  "index_patterns": ["stat-*"],
  "priority": 1,
  "template": {
    "settings": {
      "number_of_shards": "${NUMBER_OF_SHARDS}",
      "refresh_interval": "${REFRESH_INTERVAL}"
    },
    "mappings": {
      "dynamic_templates": [
        {
          "stats": {
            "path_match": "stats.*",
            "mapping": {
              "type": "scaled_float",
              "scaling_factor": 1000
            }
          }
        },
        {
          "info": {
            "path_match": "info.*",
            "mapping": {
              "type": "text",
              "index": "false"
            }
          }
        }
      ],
      "properties": {
        "@timestamp": {
          "type": "date",
          "format": "strict_date_optional_time"
        },
        "app": {
          "type": "keyword"
        },
        "host": {
          "type": "keyword"
        },
        "result": {
          "type": "keyword"
        },
        "error_code": {
          "type": "keyword"
        },
        "error_message": {
          "type": "text",
          "index": "false"
        }
      }
    }
  }
}
```
### event
```
{
  "index_patterns": ["stat-*"],
  "priority": 1,
  "template": {
    "settings": {
      "number_of_shards": "${NUMBER_OF_SHARDS}",
      "refresh_interval": "${REFRESH_INTERVAL}"
    },
    "mappings": {
      "dynamic_templates": [
        {
          "stats": {
            "path_match": "stats.*",
            "mapping": {
              "type": "scaled_float",
              "scaling_factor": 1000
            }
          }
        },
        {
          "info": {
            "path_match": "info.*",
            "mapping": {
              "type": "text",
              "index": "false"
            }
          }
        }
      ],
      "properties": {
        "@timestamp": {
          "type": "date",
          "format": "strict_date_optional_time"
        },
        "app": {
          "type": "keyword"
        },
        "host": {
          "type": "keyword"
        },
        "result": {
          "type": "keyword"
        },
        "error_code": {
          "type": "keyword"
        },
        "error_message": {
          "type": "text",
          "index": "false"
        }
      }
    }
  }
}
```
### kibana pattern
```
[
  {
    "id": "context-log-pattern", "type": "index-pattern",
    "attributes": {
      "fieldFormatMap": "{\n  \"perf_stats.http.read_entries\": {\"id\": \"bytes\", \"params\": {\"pattern\": \"0,0.[00]b\"}},\n  \"perf_stats.http.write_entries\": {\"id\": \"bytes\", \"params\": {\"pattern\": \"0,0.[00]b\"}},\n  \"stats.request_body_length\": {\"id\": \"bytes\", \"params\": {\"pattern\": \"0,0.[00]b\"}},\n  \"stats.response_body_length\": {\"id\": \"bytes\", \"params\": {\"pattern\": \"0,0.[00]b\"}},\n  \"elapsed\": {\"id\": \"duration\", \"params\": {\"inputFormat\": \"nanoseconds\", \"outputFormat\": \"humanizePrecise\", \"useShortSuffix\": true, \"outputPrecision\": 3}},\n  \"perf_stats.db.total_elapsed\": {\"id\": \"duration\", \"params\": {\"inputFormat\": \"nanoseconds\", \"outputFormat\": \"humanizePrecise\", \"useShortSuffix\": true, \"outputPrecision\": 3}},\n  \"perf_stats.elasticsearch.total_elapsed\": {\"id\": \"duration\", \"params\": {\"inputFormat\": \"nanoseconds\", \"outputFormat\": \"humanizePrecise\", \"useShortSuffix\": true, \"outputPrecision\": 3}},\n  \"perf_stats.http.total_elapsed\": {\"id\": \"duration\", \"params\": {\"inputFormat\": \"nanoseconds\", \"outputFormat\": \"humanizePrecise\", \"useShortSuffix\": true, \"outputPrecision\": 3}},\n  \"perf_stats.http_dns.total_elapsed\": {\"id\": \"duration\", \"params\": {\"inputFormat\": \"nanoseconds\", \"outputFormat\": \"humanizePrecise\", \"useShortSuffix\": true, \"outputPrecision\": 3}},\n  \"perf_stats.kafka.total_elapsed\": {\"id\": \"duration\", \"params\": {\"inputFormat\": \"nanoseconds\", \"outputFormat\": \"humanizePrecise\", \"useShortSuffix\": true, \"outputPrecision\": 3}},\n  \"perf_stats.redis.total_elapsed\": {\"id\": \"duration\", \"params\": {\"inputFormat\": \"nanoseconds\", \"outputFormat\": \"humanizePrecise\", \"useShortSuffix\": true, \"outputPrecision\": 3}},\n  \"perf_stats.mongo.total_elapsed\": {\"id\": \"duration\", \"params\": {\"inputFormat\": \"nanoseconds\", \"outputFormat\": \"humanizePrecise\", \"useShortSuffix\": true, \"outputPrecision\": 3}},\n  \"stats.cpu_time\": {\"id\": \"duration\", \"params\": {\"inputFormat\": \"nanoseconds\", \"outputFormat\": \"humanizePrecise\", \"useShortSuffix\": true, \"outputPrecision\": 3}},\n  \"stats.http_delay\": {\"id\": \"duration\", \"params\": {\"inputFormat\": \"nanoseconds\", \"outputFormat\": \"humanizePrecise\", \"useShortSuffix\": true, \"outputPrecision\": 3}},\n  \"stats.consumer_delay\": {\"id\": \"duration\", \"params\": {\"inputFormat\": \"nanoseconds\", \"outputFormat\": \"humanizePrecise\", \"useShortSuffix\": true, \"outputPrecision\": 3}},\n  \"stats.task_delay\": {\"id\": \"duration\", \"params\": {\"inputFormat\": \"nanoseconds\", \"outputFormat\": \"humanizePrecise\", \"useShortSuffix\": true, \"outputPrecision\": 3}}\n}",
      "fields": "[\n  {\"name\": \"@timestamp\", \"type\": \"date\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"_id\", \"type\": \"string\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": false},\n  {\"name\": \"action\", \"type\": \"string\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"app\", \"type\": \"string\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"client\", \"type\": \"string\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"correlation_id\", \"type\": \"string\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"ref_id\", \"type\": \"string\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"result\", \"type\": \"string\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"host\", \"type\": \"string\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"elapsed\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"error_code\", \"type\": \"string\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"error_message\", \"type\": \"string\", \"searchable\": false, \"aggregatable\": false, \"readFromDocValues\": false},\n  {\"name\": \"context.client_ip\", \"type\": \"string\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"context.controller\", \"type\": \"string\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"context.method\", \"type\": \"string\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"context.path_pattern\", \"type\": \"string\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"context.request_url\", \"type\": \"string\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"context.response_code\", \"type\": \"string\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"context.session_hash\", \"type\": \"string\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"context.user_agent\", \"type\": \"string\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"context.referer\", \"type\": \"string\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"context.topic\", \"type\": \"string\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"context.key\", \"type\": \"string\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"context.handler\", \"type\": \"string\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"context.trigger\", \"type\": \"string\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"context.job\", \"type\": \"string\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"context.job_class\", \"type\": \"string\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"perf_stats.db.count\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"perf_stats.db.total_elapsed\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"perf_stats.db.read_entries\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"perf_stats.db.write_entries\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"perf_stats.elasticsearch.count\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"perf_stats.elasticsearch.total_elapsed\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"perf_stats.elasticsearch.read_entries\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"perf_stats.elasticsearch.write_entries\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"perf_stats.http.count\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"perf_stats.http.total_elapsed\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"perf_stats.http.read_entries\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"perf_stats.http.write_entries\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"perf_stats.http_dns.count\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"perf_stats.http_dns.total_elapsed\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"perf_stats.http_conn.count\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"perf_stats.http_conn.total_elapsed\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"perf_stats.kafka.count\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"perf_stats.kafka.total_elapsed\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"perf_stats.kafka.read_entries\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"perf_stats.kafka.write_entries\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"perf_stats.redis.count\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"perf_stats.redis.total_elapsed\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"perf_stats.redis.read_entries\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"perf_stats.redis.write_entries\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"perf_stats.mongo.total_elapsed\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.cpu_time\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.request_body_length\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.response_body_length\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.http_delay\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.http_retries\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.consumer_delay\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.task_delay\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.cache_hits\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.cache_misses\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.db_queries\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.customer_registered\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.order_placed\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.order_amount\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true}\n]",
      "timeFieldName": "@timestamp",
      "title": "action-*"
    }
  },
  {
    "id": "stat-pattern", "type": "index-pattern",
    "attributes": {
      "fieldFormatMap": "{\n  \"stats.cpu_usage\": {\"id\": \"percent\", \"params\": {}},\n  \"stats.jvm_heap_used\": {\"id\": \"bytes\", \"params\": {\"pattern\": \"0,0.[00]b\"}},\n  \"stats.jvm_heap_max\": {\"id\": \"bytes\", \"params\": {\"pattern\": \"0,0.[00]b\"}},\n  \"stats.jvm_non_heap_used\": {\"id\": \"bytes\", \"params\": {\"pattern\": \"0,0.[00]b\"}},\n  \"stats.vm_rss\": {\"id\": \"bytes\", \"params\": {\"pattern\": \"0,0.[00]b\"}},\n  \"stats.mem_max\": {\"id\": \"bytes\", \"params\": {\"pattern\": \"0,0.[00]b\"}},\n  \"stats.kafka_consumer_bytes_consumed_rate\": {\"id\": \"bytes\", \"params\": {\"pattern\": \"0,0.[00]b\"}},\n  \"stats.kafka_producer_log-forwarder_outgoing_byte_rate\": {\"id\": \"bytes\", \"params\": {\"pattern\": \"0,0.[00]b\"}},\n  \"stats.kafka_producer_log-forwarder_request_size_avg\": {\"id\": \"bytes\", \"params\": {\"pattern\": \"0,0.[00]b\"}},\n  \"stats.kafka_producer_outgoing_byte_rate\": {\"id\": \"bytes\", \"params\": {\"pattern\": \"0,0.[00]b\"}},\n  \"stats.kafka_producer_request_size_avg\": {\"id\": \"bytes\", \"params\": {\"pattern\": \"0,0.[00]b\"}},\n  \"stats.kafka_producer_request_size_max\": {\"id\": \"bytes\", \"params\": {\"pattern\": \"0,0.[00]b\"}},\n  \"stats.kafka_max_message_size\": {\"id\": \"bytes\", \"params\": {\"pattern\": \"0,0.[00]b\"}},\n  \"stats.kafka_heap_used\": {\"id\": \"bytes\", \"params\": {\"pattern\": \"0,0.[00]b\"}},\n  \"stats.kafka_heap_max\": {\"id\": \"bytes\", \"params\": {\"pattern\": \"0,0.[00]b\"}},\n  \"stats.kafka_non_heap_used\": {\"id\": \"bytes\", \"params\": {\"pattern\": \"0,0.[00]b\"}},\n  \"stats.kafka_bytes_out_rate\": {\"id\": \"bytes\", \"params\": {\"pattern\": \"0,0.[00]b\"}},\n  \"stats.kafka_bytes_in_rate\": {\"id\": \"bytes\", \"params\": {\"pattern\": \"0,0.[00]b\"}},\n  \"stats.kafka_disk_used\": {\"id\": \"bytes\", \"params\": {\"pattern\": \"0,0.[00]b\"}},\n  \"stats.redis_mem_used\": {\"id\": \"bytes\", \"params\": {\"pattern\": \"0,0.[00]b\"}},\n  \"stats.redis_mem_max\": {\"id\": \"bytes\", \"params\": {\"pattern\": \"0,0.[00]b\"}},\n  \"stats.es_cpu_usage\": {\"id\": \"percent\", \"params\": {}},\n  \"stats.es_disk_used\": {\"id\": \"bytes\", \"params\": {\"pattern\": \"0,0.[00]b\"}},\n  \"stats.es_disk_max\": {\"id\": \"bytes\", \"params\": {\"pattern\": \"0,0.[00]b\"}},\n  \"stats.es_heap_used\": {\"id\": \"bytes\", \"params\": {\"pattern\": \"0,0.[00]b\"}},\n  \"stats.es_heap_max\": {\"id\": \"bytes\", \"params\": {\"pattern\": \"0,0.[00]b\"}},\n  \"stats.es_non_heap_used\": {\"id\": \"bytes\", \"params\": {\"pattern\": \"0,0.[00]b\"}}\n}",
      "fields": "[\n  {\"name\": \"@timestamp\", \"type\": \"date\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"_id\", \"type\": \"string\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": false},\n  {\"name\": \"app\", \"type\": \"string\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"host\", \"type\": \"string\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"result\", \"type\": \"string\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"error_code\", \"type\": \"string\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"error_message\", \"type\": \"string\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.cpu_usage\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.sys_load_avg\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.thread_count\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.jvm_gc_old_count\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.jvm_gc_old_elapsed\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.jvm_gc_young_count\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.jvm_gc_young_elapsed\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.jvm_heap_used\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.jvm_heap_max\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.jvm_non_heap_used\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.vm_rss\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.mem_max\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.http_active_requests\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.kafka_consumer_bytes_consumed_rate\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.kafka_consumer_fetch_rate\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.kafka_consumer_records_consumed_rate\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.kafka_consumer_records_max_lag\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.kafka_producer_log-forwarder_outgoing_byte_rate\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.kafka_producer_log-forwarder_request_rate\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.kafka_producer_log-forwarder_request_size_avg\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.kafka_producer_outgoing_byte_rate\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.kafka_producer_request_rate\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.kafka_producer_request_size_avg\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.kafka_producer_request_size_max\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.kafka_max_message_size\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.kafka_heap_used\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.kafka_heap_max\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.kafka_non_heap_used\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.kafka_gc_young_count\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.kafka_gc_young_elapsed\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.kafka_gc_old_count\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.kafka_gc_old_elapsed\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.kafka_bytes_out_rate\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.kafka_bytes_in_rate\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.pool_db_active_count\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.pool_db_total_count\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.pool_redis-cache_active_count\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.pool_redis-cache_total_count\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.pool_redis-session_active_count\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.pool_redis-session_total_count\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.pool_redis_active_count\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.pool_redis_total_count\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.cache_size\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.redis_mem_used\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.redis_mem_max\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.redis_keys\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.es_cpu_usage\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.es_disk_used\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.es_disk_max\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.es_heap_used\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.es_heap_max\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.es_non_heap_used\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.es_gc_young_count\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.es_gc_young_elapsed\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.es_gc_old_count\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.es_gc_old_elapsed\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"stats.es_docs\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true}\n]",
      "timeFieldName": "@timestamp",
      "title": "stat-*"
    }
  },
  {
    "id": "trace-pattern", "type": "index-pattern",
    "attributes": {
      "fields": "[\n  {\"name\": \"@timestamp\", \"type\": \"date\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"action\", \"type\": \"string\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"app\", \"type\": \"string\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"content\", \"type\": \"string\", \"searchable\": false, \"aggregatable\": false, \"readFromDocValues\": false},\n  {\"name\": \"error_code\", \"type\": \"string\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"result\", \"type\": \"string\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true}\n]",
      "timeFieldName": "@timestamp",
      "title": "trace-*"
    }
  },
  {
    "id": "event-pattern", "type": "index-pattern",
    "attributes": {
      "fields": "[\n  {\"name\": \"@timestamp\", \"type\": \"date\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"_id\", \"type\": \"string\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": false},\n  {\"name\": \"action\", \"type\": \"string\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"app\", \"type\": \"string\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"received_time\", \"type\": \"date\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"error_code\", \"type\": \"string\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"error_message\", \"type\": \"string\", \"searchable\": false, \"aggregatable\": false, \"readFromDocValues\": false},\n  {\"name\": \"elapsed\", \"type\": \"number\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"result\", \"type\": \"string\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"context.client_ip\", \"type\": \"string\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true},\n  {\"name\": \"context.user_agent\", \"type\": \"string\", \"searchable\": true, \"aggregatable\": true, \"readFromDocValues\": true}\n]\n",
      "timeFieldName": "@timestamp",
      "title": "event-*"
    }
  }
]
```
