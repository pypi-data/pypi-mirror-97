# Install
```shell script
# Elasticsearch 7.x
pip install "namekox-elasticsearch>=7.0.0,<8.0.0"
# Elasticsearch 6.x
pip install "namekox-elasticsearch>=6.0.0,<7.0.0"
# Elasticsearch 5.x
pip install "namekox-elasticsearch>=5.0.0,<6.0.0"
# Elasticsearch 2.x
pip install "namekox-elasticsearch>=2.0.0,<3.0.0"
```

# Example
```python
#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals


from elasticsearch_dsl.connections import connections
from namekox_webserver.core.entrypoints.app import app
from namekox_elasticsearch.core.dependencies import ElasticSearchHelper


class Ping(object):
    name = 'ping'

    # https://elasticsearch-dsl.readthedocs.io/en/latest/index.html
    test_es = ElasticSearchHelper('test')
    prod_es = ElasticSearchHelper('prod')

    @app.api('/api/<any(test,prod):env>/cluster/health/', methods=['GET'])
    def cluster_health(self, request, env):
        connection = connections.get_connection(env)
        return connection.cluster.health()
```

# Running
> config.yaml
```yaml
ELASTICSEARCH:
  test:
    hosts:
      - 10.0.0.1:9200
    sniff_on_start: true
  prod:
    hosts:
      - 10.0.0.2:9200
    sniff_on_start: true
```
> namekox run ping
```shell script
2021-02-26 11:39:34,065 DEBUG load container class from namekox_core.core.service.container:ServiceContainer
2021-02-26 11:39:34,066 DEBUG starting services [u'ping']
2021-02-26 11:39:34,066 DEBUG starting service ping entrypoints [ping:namekox_webserver.core.entrypoints.app.handler.ApiServerHandler:cluster_health, ping:namekox_webserver.core.entrypoints.app.server.WebServer:server]
2021-02-26 11:39:34,069 DEBUG spawn manage thread handle ping:namekox_webserver.core.entrypoints.app.server:handle_connect(args=(), kwargs={}, tid=handle_connect)
2021-02-26 11:39:34,069 DEBUG service ping entrypoints [ping:namekox_webserver.core.entrypoints.app.handler.ApiServerHandler:cluster_health, ping:namekox_webserver.core.entrypoints.app.server.WebServer:server] started
2021-02-26 11:39:34,069 DEBUG starting service ping dependencies [ping:namekox_elasticsearch.core.dependencies.ElasticSearchHelper:prod_es]
2021-02-26 11:39:34,069 DEBUG Starting new HTTP connection (1): 10.0.0.2:9200
2021-02-26 11:39:34,080 DEBUG http://10.0.0.2:9200 "GET /_nodes/_all/http HTTP/1.1" 200 5016
2021-02-26 11:39:34,081 INFO GET http://10.0.0.2:9200/_nodes/_all/http [status:200 request:0.011s]
2021-02-26 11:39:34,081 DEBUG > None
2021-02-26 11:39:34,081 DEBUG < {"_nodes":{"total":10,"successful":10,"failed":0},"cluster_name":"elk-stack","nodes":{"1WBgg6WsQyy--JucGzSEMw":{"name":"es-data03","transport_address":"10.246.102.58:9300","host":"10.246.102.58","ip":"10.246.102.58","version":"6.8.0","build_flavor":"default","build_type":"tar","build_hash":"65b6179","roles":["data"],"attributes":{"ml.machine_memory":"16656113664","ml.max_open_jobs":"20","box_type":"cold","xpack.installed":"true","ml.enabled":"true"},"http":{"bound_address":["10.246.102.58:9200"],"publish_address":"10.246.102.58:9200","max_content_length_in_bytes":104857600}},"fjD8TH3bRSqYiYCUcIgYaQ":{"name":"es-data05","transport_address":"10.246.83.11:9300","host":"10.246.83.11","ip":"10.246.83.11","version":"6.8.0","build_flavor":"default","build_type":"tar","build_hash":"65b6179","roles":["data"],"attributes":{"ml.machine_memory":"16650412032","ml.max_open_jobs":"20","box_type":"cold","xpack.installed":"true","ml.enabled":"true"},"http":{"bound_address":["10.246.83.11:9200"],"publish_address":"10.246.83.11:9200","max_content_length_in_bytes":104857600}},"a_8zwirYSrKAuh9AANYaYA":{"name":"es-matser01","transport_address":"10.246.102.51:9300","host":"10.246.102.51","ip":"10.246.102.51","version":"6.8.0","build_flavor":"default","build_type":"tar","build_hash":"65b6179","roles":["master","ingest"],"attributes":{"ml.machine_memory":"8201060352","ml.max_open_jobs":"20","xpack.installed":"true","ml.enabled":"true"},"http":{"bound_address":["10.246.102.51:9200"],"publish_address":"10.246.102.51:9200","max_content_length_in_bytes":104857600}},"f6kgv_cuTvOgHDuxU8GQjw":{"name":"es-data01","transport_address":"10.246.102.52:9300","host":"10.246.102.52","ip":"10.246.102.52","version":"6.8.0","build_flavor":"default","build_type":"tar","build_hash":"65b6179","roles":["data"],"attributes":{"ml.machine_memory":"16656113664","ml.max_open_jobs":"20","xpack.installed":"true","box_type":"hot","ml.enabled":"true"},"http":{"bound_address":["10.246.102.52:9200"],"publish_address":"10.246.102.52:9200","max_content_length_in_bytes":104857600}},"86Txc3tBSVWZhd3ZK4e39Q":{"name":"es-data04","transport_address":"10.246.102.74:9300","host":"10.246.102.74","ip":"10.246.102.74","version":"6.8.0","build_flavor":"default","build_type":"tar","build_hash":"65b6179","roles":["data"],"attributes":{"ml.machine_memory":"16655851520","ml.max_open_jobs":"20","box_type":"cold","xpack.installed":"true","ml.enabled":"true"},"http":{"bound_address":["10.246.102.74:9200"],"publish_address":"10.246.102.74:9200","max_content_length_in_bytes":104857600}},"m5ny37WtT_agzNyijDkNIQ":{"name":"es-master02","transport_address":"10.246.102.56:9300","host":"10.246.102.56","ip":"10.246.102.56","version":"6.8.0","build_flavor":"default","build_type":"tar","build_hash":"65b6179","roles":["master","ingest"],"attributes":{"ml.machine_memory":"8201056256","ml.max_open_jobs":"20","xpack.installed":"true","ml.enabled":"true"},"http":{"bound_address":["10.246.102.56:9200"],"publish_address":"10.246.102.56:9200","max_content_length_in_bytes":104857600}},"AV-L8GE3Sp-Af0EaGGtJ6Q":{"name":"es-data06","transport_address":"10.246.83.44:9300","host":"10.246.83.44","ip":"10.246.83.44","version":"6.8.0","build_flavor":"default","build_type":"tar","build_hash":"65b6179","roles":["data"],"attributes":{"ml.machine_memory":"16783376384","ml.max_open_jobs":"20","xpack.installed":"true","box_type":"hot","ml.enabled":"true"},"http":{"bound_address":["10.246.83.44:9200"],"publish_address":"10.246.83.44:9200","max_content_length_in_bytes":104857600}},"v9Fa3zLPQDaZ-_F_0tLXGg":{"name":"es-master03","transport_address":"10.0.0.2:9300","host":"10.0.0.2","ip":"10.0.0.2","version":"6.8.0","build_flavor":"default","build_type":"tar","build_hash":"65b6179","roles":["master","ingest"],"attributes":{"ml.machine_memory":"25239089152","xpack.installed":"true","ml.max_open_jobs":"20","ml.enabled":"true"},"http":{"bound_address":["10.0.0.2:9200"],"publish_address":"10.0.0.2:9200","max_content_length_in_bytes":104857600}},"W0d9l4BgSMKwW-v0ecP2eg":{"name":"es-data02","transport_address":"10.246.102.57:9300","host":"10.246.102.57","ip":"10.246.102.57","version":"6.8.0","build_flavor":"default","build_type":"tar","build_hash":"65b6179","roles":["data"],"attributes":{"ml.machine_memory":"16656113664","ml.max_open_jobs":"20","box_type":"hot","xpack.installed":"true","ml.enabled":"true"},"http":{"bound_address":["10.246.102.57:9200"],"publish_address":"10.246.102.57:9200","max_content_length_in_bytes":104857600}},"ZlGK722mSHCvZ7Fw_snu1Q":{"name":"es-data07","transport_address":"10.246.102.125:9300","host":"10.246.102.125","ip":"10.246.102.125","version":"6.8.0","build_flavor":"default","build_type":"tar","build_hash":"65b6179","roles":["data"],"attributes":{"ml.machine_memory":"17076531200","ml.max_open_jobs":"20","xpack.installed":"true","box_type":"hot","ml.enabled":"true"},"http":{"bound_address":["10.246.102.125:9200"],"publish_address":"10.246.102.125:9200","max_content_length_in_bytes":104857600}}}}
2021-02-26 11:39:34,085 DEBUG service ping dependencies [ping:namekox_elasticsearch.core.dependencies.ElasticSearchHelper:prod_es] started
2021-02-26 11:39:34,085 DEBUG services [u'ping'] started
2021-02-26 11:39:40,167 DEBUG spawn manage thread handle ping:namekox_webserver.core.entrypoints.app.server:handle_request(args=(<eventlet.greenio.base.GreenSocket object at 0x1083fde10>, ('127.0.0.1', 60078)), kwargs={}, tid=handle_request)
2021-02-26 11:39:40,168 DEBUG spawn worker thread handle ping:cluster_health(args=(<Request 'http://127.0.0.1/api/prod/cluster/health/' [GET]>,), kwargs={'env': u'prod'}, context={})
2021-02-26 11:39:40,193 DEBUG http://10.0.0.2:9200 "GET /_cluster/health HTTP/1.1" 200 392
2021-02-26 11:39:40,194 INFO GET http://10.0.0.2:9200/_cluster/health [status:200 request:0.025s]
2021-02-26 11:39:40,194 DEBUG > None
2021-02-26 11:39:40,194 DEBUG < {"cluster_name":"elk-stack","status":"green","timed_out":false,"number_of_nodes":10,"number_of_data_nodes":7,"active_primary_shards":3647,"active_shards":4593,"relocating_shards":0,"initializing_shards":0,"unassigned_shards":0,"delayed_unassigned_shards":0,"number_of_pending_tasks":0,"number_of_in_flight_fetch":0,"task_max_waiting_in_queue_millis":0,"active_shards_percent_as_number":100.0}
127.0.0.1 - - [26/Feb/2021 11:39:40] "GET /api/prod/cluster/health/ HTTP/1.1" 200 654 0.027814
^C2021-02-26 11:39:49,392 DEBUG stopping services [u'ping']
2021-02-26 11:39:49,392 DEBUG stopping service ping entrypoints [ping:namekox_webserver.core.entrypoints.app.handler.ApiServerHandler:cluster_health, ping:namekox_webserver.core.entrypoints.app.server.WebServer:server]
2021-02-26 11:39:49,393 DEBUG wait service ping entrypoints [ping:namekox_webserver.core.entrypoints.app.handler.ApiServerHandler:cluster_health, ping:namekox_webserver.core.entrypoints.app.server.WebServer:server] stop
2021-02-26 11:39:49,394 DEBUG service ping entrypoints [ping:namekox_webserver.core.entrypoints.app.handler.ApiServerHandler:cluster_health, ping:namekox_webserver.core.entrypoints.app.server.WebServer:server] stopped
2021-02-26 11:39:49,394 DEBUG stopping service ping dependencies [ping:namekox_elasticsearch.core.dependencies.ElasticSearchHelper:prod_es]
2021-02-26 11:39:49,395 DEBUG service ping dependencies [ping:namekox_elasticsearch.core.dependencies.ElasticSearchHelper:prod_es] stopped
2021-02-26 11:39:49,395 DEBUG services [u'ping'] stopped
2021-02-26 11:39:49,396 DEBUG killing services [u'ping']
2021-02-26 11:39:49,396 DEBUG service ping already stopped
2021-02-26 11:39:49,397 DEBUG services [u'ping'] killed
```
> curl http://127.0.0.1/api/prod/cluster/health/
```json5
{
    "errs": "",
    "code": "Request:Success",
    "data": {
        "status": "green",
        "number_of_nodes": 10,
        "unassigned_shards": 0,
        "number_of_pending_tasks": 0,
        "number_of_in_flight_fetch": 0,
        "timed_out": false,
        "active_primary_shards": 3647,
        "task_max_waiting_in_queue_millis": 0,
        "cluster_name": "elk-stack",
        "relocating_shards": 0,
        "active_shards_percent_as_number": 100,
        "active_shards": 4593,
        "initializing_shards": 0,
        "number_of_data_nodes": 7,
        "delayed_unassigned_shards": 0
    },
    "call_id": "06f46903-cb0e-41b1-945a-3de87f446793"
}
```

# Debug
> config.yaml
```yaml
CONTEXT:
  - namekox_elasticsearch.cli.subctx.elasticsearch:ElasticSearch
ELASTICSEARCH:
  test:
    hosts:
      - 10.0.0.1:9200
    sniff_on_start: true
  prod:
    hosts:
      - 10.0.0.2:9200
    sniff_on_start: true
```
> namekox shell
```shell script
Namekox Python 2.7.16 (default, Jun  5 2020, 22:59:21)
[GCC 4.2.1 Compatible Apple LLVM 11.0.3 (clang-1103.0.29.20) (-macos10.15-objc- shell on darwin
In [1]: es = nx.elasticsearch.proxy('prod')
2021-02-26 11:52:49,703 DEBUG Starting new HTTP connection (1): 10.0.0.2:9200
2021-02-26 11:52:49,716 DEBUG http://10.0.0.2:9200 "GET /_nodes/_all/http HTTP/1.1" 200 5016
2021-02-26 11:52:49,717 INFO GET http://10.0.0.2:9200/_nodes/_all/http [status:200 request:0.014s]
2021-02-26 11:52:49,717 DEBUG > None
2021-02-26 11:52:49,717 DEBUG < {"_nodes":{"total":10,"successful":10,"failed":0},"cluster_name":"elk-stack","nodes":{"W0d9l4BgSMKwW-v0ecP2eg":{"name":"es-data02","transport_address":"10.246.102.57:9300","host":"10.246.102.57","ip":"10.246.102.57","version":"6.8.0","build_flavor":"default","build_type":"tar","build_hash":"65b6179","roles":["data"],"attributes":{"ml.machine_memory":"16656113664","ml.max_open_jobs":"20","box_type":"hot","xpack.installed":"true","ml.enabled":"true"},"http":{"bound_address":["10.246.102.57:9200"],"publish_address":"10.246.102.57:9200","max_content_length_in_bytes":104857600}},"86Txc3tBSVWZhd3ZK4e39Q":{"name":"es-data04","transport_address":"10.246.102.74:9300","host":"10.246.102.74","ip":"10.246.102.74","version":"6.8.0","build_flavor":"default","build_type":"tar","build_hash":"65b6179","roles":["data"],"attributes":{"ml.machine_memory":"16655851520","ml.max_open_jobs":"20","box_type":"cold","xpack.installed":"true","ml.enabled":"true"},"http":{"bound_address":["10.246.102.74:9200"],"publish_address":"10.246.102.74:9200","max_content_length_in_bytes":104857600}},"v9Fa3zLPQDaZ-_F_0tLXGg":{"name":"es-master03","transport_address":"10.0.0.2:9300","host":"10.0.0.2","ip":"10.0.0.2","version":"6.8.0","build_flavor":"default","build_type":"tar","build_hash":"65b6179","roles":["master","ingest"],"attributes":{"ml.machine_memory":"25239089152","xpack.installed":"true","ml.max_open_jobs":"20","ml.enabled":"true"},"http":{"bound_address":["10.0.0.2:9200"],"publish_address":"10.0.0.2:9200","max_content_length_in_bytes":104857600}},"AV-L8GE3Sp-Af0EaGGtJ6Q":{"name":"es-data06","transport_address":"10.246.83.44:9300","host":"10.246.83.44","ip":"10.246.83.44","version":"6.8.0","build_flavor":"default","build_type":"tar","build_hash":"65b6179","roles":["data"],"attributes":{"ml.machine_memory":"16783376384","ml.max_open_jobs":"20","xpack.installed":"true","box_type":"hot","ml.enabled":"true"},"http":{"bound_address":["10.246.83.44:9200"],"publish_address":"10.246.83.44:9200","max_content_length_in_bytes":104857600}},"ZlGK722mSHCvZ7Fw_snu1Q":{"name":"es-data07","transport_address":"10.246.102.125:9300","host":"10.246.102.125","ip":"10.246.102.125","version":"6.8.0","build_flavor":"default","build_type":"tar","build_hash":"65b6179","roles":["data"],"attributes":{"ml.machine_memory":"17076531200","ml.max_open_jobs":"20","xpack.installed":"true","box_type":"hot","ml.enabled":"true"},"http":{"bound_address":["10.246.102.125:9200"],"publish_address":"10.246.102.125:9200","max_content_length_in_bytes":104857600}},"a_8zwirYSrKAuh9AANYaYA":{"name":"es-matser01","transport_address":"10.246.102.51:9300","host":"10.246.102.51","ip":"10.246.102.51","version":"6.8.0","build_flavor":"default","build_type":"tar","build_hash":"65b6179","roles":["master","ingest"],"attributes":{"ml.machine_memory":"8201060352","ml.max_open_jobs":"20","xpack.installed":"true","ml.enabled":"true"},"http":{"bound_address":["10.246.102.51:9200"],"publish_address":"10.246.102.51:9200","max_content_length_in_bytes":104857600}},"f6kgv_cuTvOgHDuxU8GQjw":{"name":"es-data01","transport_address":"10.246.102.52:9300","host":"10.246.102.52","ip":"10.246.102.52","version":"6.8.0","build_flavor":"default","build_type":"tar","build_hash":"65b6179","roles":["data"],"attributes":{"ml.machine_memory":"16656113664","ml.max_open_jobs":"20","xpack.installed":"true","box_type":"hot","ml.enabled":"true"},"http":{"bound_address":["10.246.102.52:9200"],"publish_address":"10.246.102.52:9200","max_content_length_in_bytes":104857600}},"1WBgg6WsQyy--JucGzSEMw":{"name":"es-data03","transport_address":"10.246.102.58:9300","host":"10.246.102.58","ip":"10.246.102.58","version":"6.8.0","build_flavor":"default","build_type":"tar","build_hash":"65b6179","roles":["data"],"attributes":{"ml.machine_memory":"16656113664","ml.max_open_jobs":"20","box_type":"cold","xpack.installed":"true","ml.enabled":"true"},"http":{"bound_address":["10.246.102.58:9200"],"publish_address":"10.246.102.58:9200","max_content_length_in_bytes":104857600}},"fjD8TH3bRSqYiYCUcIgYaQ":{"name":"es-data05","transport_address":"10.246.83.11:9300","host":"10.246.83.11","ip":"10.246.83.11","version":"6.8.0","build_flavor":"default","build_type":"tar","build_hash":"65b6179","roles":["data"],"attributes":{"ml.machine_memory":"16650412032","ml.max_open_jobs":"20","box_type":"cold","xpack.installed":"true","ml.enabled":"true"},"http":{"bound_address":["10.246.83.11:9200"],"publish_address":"10.246.83.11:9200","max_content_length_in_bytes":104857600}},"m5ny37WtT_agzNyijDkNIQ":{"name":"es-master02","transport_address":"10.246.102.56:9300","host":"10.246.102.56","ip":"10.246.102.56","version":"6.8.0","build_flavor":"default","build_type":"tar","build_hash":"65b6179","roles":["master","ingest"],"attributes":{"ml.machine_memory":"8201056256","ml.max_open_jobs":"20","xpack.installed":"true","ml.enabled":"true"},"http":{"bound_address":["10.246.102.56:9200"],"publish_address":"10.246.102.56:9200","max_content_length_in_bytes":104857600}}}}
In [2]: from elasticsearch_dsl.connections import connections
In [3]: connection = connections.get_connection('prod')
In [4]: connection.cluster.health()
2021-02-26 11:53:36,912 DEBUG Starting new HTTP connection (1): 10.246.83.11:9200
2021-02-26 11:53:36,939 DEBUG http://10.246.83.11:9200 "GET /_cluster/health HTTP/1.1" 200 392
2021-02-26 11:53:36,941 INFO GET http://10.246.83.11:9200/_cluster/health [status:200 request:0.028s]
2021-02-26 11:53:36,941 DEBUG > None
2021-02-26 11:53:36,941 DEBUG < {"cluster_name":"elk-stack","status":"green","timed_out":false,"number_of_nodes":10,"number_of_data_nodes":7,"active_primary_shards":3647,"active_shards":4593,"relocating_shards":0,"initializing_shards":0,"unassigned_shards":0,"delayed_unassigned_shards":0,"number_of_pending_tasks":0,"number_of_in_flight_fetch":0,"task_max_waiting_in_queue_millis":0,"active_shards_percent_as_number":100.0}
Out[4]:
{u'active_primary_shards': 3647,
 u'active_shards': 4593,
 u'active_shards_percent_as_number': 100.0,
 u'cluster_name': u'elk-stack',
 u'delayed_unassigned_shards': 0,
 u'initializing_shards': 0,
 u'number_of_data_nodes': 7,
 u'number_of_in_flight_fetch': 0,
 u'number_of_nodes': 10,
 u'number_of_pending_tasks': 0,
 u'relocating_shards': 0,
 u'status': u'green',
 u'task_max_waiting_in_queue_millis': 0,
 u'timed_out': False,
 u'unassigned_shards': 0}
```
