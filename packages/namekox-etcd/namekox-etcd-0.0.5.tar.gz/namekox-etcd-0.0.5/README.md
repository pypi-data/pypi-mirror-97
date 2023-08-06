# Install
```shell script
pip install -U namekox-etcd
```

# Example
```python
# ! -*- coding: utf-8 -*-
#
# author: forcemain@163.com


from namekox_etcd.core.allotter import Allotter
from namekox_webserver.core.entrypoints.app import app
from namekox_etcd.core.dependencies.etcd3 import Etcd3Helper
from namekox_etcd.constants import DEFAULT_ETCD_SERVICE_ROOT_PATH


class Ping(object):
    name = 'ping'

    # https://github.com/Revolution1/etcd3-py
    # Etcd3Helper(
    #       dbname,
    #       serverid=None,
    #       leasettl=None,
    #       watching=None,
    #       allotter=None,
    #       coptions=None,
    #       roptions=None):
    #
    etcd3 = Etcd3Helper(name, allotter=Allotter(), watching=DEFAULT_ETCD_SERVICE_ROOT_PATH)

    @app.api('/api/assign/server/', methods=['GET'])
    def assign_server(self, request):
        return self.etcd3.allotter.get(self.name)
```

# Running
> config.yaml
```yaml
ETCD3:
  ping:
    host: 127.0.0.1
    port: 2379
WEBSERVER:
  host: 0.0.0.0
  port: 80
```
> namekox run ping
```shell script
2020-11-27 19:43:03,116 DEBUG load container class from namekox_core.core.service.container:ServiceContainer
2020-11-27 19:43:03,116 DEBUG starting services ['ping']
2020-11-27 19:43:03,117 DEBUG starting service ping entrypoints [ping:namekox_webserver.core.entrypoints.app.handler.ApiServerHandler:assign_server, ping:namekox_webserver.core.entrypoints.app.server.WebServer:server]
2020-11-27 19:43:03,119 DEBUG spawn manage thread handle ping:namekox_webserver.core.entrypoints.app.server:handle_connect(args=(), kwargs={}, tid=handle_connect)
2020-11-27 19:43:03,120 DEBUG service ping entrypoints [ping:namekox_webserver.core.entrypoints.app.handler.ApiServerHandler:assign_server, ping:namekox_webserver.core.entrypoints.app.server.WebServer:server] started
2020-11-27 19:43:03,120 DEBUG starting service ping dependencies [ping:namekox_etcd.core.dependencies.etcd3.Etcd3Helper:etcd3]
2020-11-27 19:43:03,128 DEBUG Starting new HTTP connection (1): 127.0.0.1:2379
2020-11-27 19:43:03,129 DEBUG http://127.0.0.1:2379 "GET /version HTTP/1.1" 200 45
2020-11-27 19:43:03,133 DEBUG Starting new HTTP connection (1): 127.0.0.1:2379
2020-11-27 19:43:03,135 DEBUG http://127.0.0.1:2379 "POST /v3/watch HTTP/1.1" 200 None
2020-11-27 19:43:03,136 DEBUG start watching prefix '/namekox'
2020-11-27 19:43:03,138 DEBUG got a watch response
2020-11-27 19:43:03,138 DEBUG watch request created
2020-11-27 19:43:03,144 DEBUG Starting new HTTP connection (2): 127.0.0.1:2379
2020-11-27 19:43:03,147 DEBUG got a watch response
2020-11-27 19:43:03,147 DEBUG dispatching event '<WatchEvent PUT '/namekox/ping.94b56994-a652-41c0-97f3-32bc825befca'>'
2020-11-27 19:43:03,150 DEBUG Starting new HTTP connection (3): 127.0.0.1:2379
2020-11-27 19:43:03,151 DEBUG http://127.0.0.1:2379 "POST /v3/kv/put HTTP/1.1" 200 117
2020-11-27 19:43:03,155 DEBUG service ping dependencies [ping:namekox_etcd.core.dependencies.etcd3.Etcd3Helper:etcd3] started
2020-11-27 19:43:03,155 DEBUG services ['ping'] started
2020-11-27 19:43:03,156 DEBUG http://127.0.0.1:2379 "POST /v3/kv/range HTTP/1.1" 200 334
2020-11-27 19:43:03,435 DEBUG http://127.0.0.1:2379 "POST /v3/lease/keepalive HTTP/1.1" 200 None
2020-11-27 19:43:03,438 DEBUG keeping lease 0
2020-11-27 19:43:04,743 DEBUG Resetting dropped connection: 127.0.0.1
2020-11-27 19:43:04,746 DEBUG http://127.0.0.1:2379 "POST /v3/lease/keepalive HTTP/1.1" 200 None
2020-11-27 19:43:04,748 DEBUG keeping lease 0
2020-11-27 19:43:06,062 DEBUG Resetting dropped connection: 127.0.0.1
2020-11-27 19:43:06,064 DEBUG http://127.0.0.1:2379 "POST /v3/lease/keepalive HTTP/1.1" 200 None
2020-11-27 19:43:06,067 DEBUG keeping lease 0
2020-11-27 19:43:07,371 DEBUG Resetting dropped connection: 127.0.0.1
2020-11-27 19:43:07,374 DEBUG http://127.0.0.1:2379 "POST /v3/lease/keepalive HTTP/1.1" 200 None
2020-11-27 19:43:07,376 DEBUG keeping lease 0
2020-11-27 19:43:07,977 DEBUG spawn manage thread handle ping:namekox_webserver.core.entrypoints.app.server:handle_request(args=(<eventlet.greenio.base.GreenSocket object at 0x103da7190>, ('127.0.0.1', 56122)), kwargs={}, tid=handle_request)
2020-11-27 19:43:07,979 DEBUG spawn worker thread handle ping:assign_server(args=(<Request 'http://127.0.0.1/api/assign/server/' [GET]>,), kwargs={}, context={})
127.0.0.1 - - [27/Nov/2020 19:43:07] "GET /api/assign/server/ HTTP/1.1" 200 269 0.001890
2020-11-27 19:43:08,684 DEBUG Resetting dropped connection: 127.0.0.1
2020-11-27 19:43:08,686 DEBUG http://127.0.0.1:2379 "POST /v3/lease/keepalive HTTP/1.1" 200 None
2020-11-27 19:43:08,688 DEBUG keeping lease 0
2020-11-27 19:43:09,992 DEBUG Resetting dropped connection: 127.0.0.1
2020-11-27 19:43:09,994 DEBUG http://127.0.0.1:2379 "POST /v3/lease/keepalive HTTP/1.1" 200 None
2020-11-27 19:43:09,996 DEBUG keeping lease 0
^C2020-11-27 19:43:10,444 DEBUG stopping services ['ping']
2020-11-27 19:43:10,445 DEBUG stopping service ping entrypoints [ping:namekox_webserver.core.entrypoints.app.handler.ApiServerHandler:assign_server, ping:namekox_webserver.core.entrypoints.app.server.WebServer:server]
2020-11-27 19:43:10,446 DEBUG wait service ping entrypoints [ping:namekox_webserver.core.entrypoints.app.handler.ApiServerHandler:assign_server, ping:namekox_webserver.core.entrypoints.app.server.WebServer:server] stop
2020-11-27 19:43:10,446 DEBUG service ping entrypoints [ping:namekox_webserver.core.entrypoints.app.handler.ApiServerHandler:assign_server, ping:namekox_webserver.core.entrypoints.app.server.WebServer:server] stopped
2020-11-27 19:43:10,446 DEBUG stopping service ping dependencies [ping:namekox_etcd.core.dependencies.etcd3.Etcd3Helper:etcd3]
2020-11-27 19:43:10,446 DEBUG stop watching
2020-11-27 19:43:10,446 DEBUG closing response stream
2020-11-27 19:43:10,447 DEBUG stop watching
2020-11-27 19:43:10,497 DEBUG canceled keeping lease 0
2020-11-27 19:43:10,497 DEBUG revoking lease 0
2020-11-27 19:43:10,499 DEBUG Resetting dropped connection: 127.0.0.1
2020-11-27 19:43:10,501 DEBUG http://127.0.0.1:2379 "POST /v3/kv/lease/revoke HTTP/1.1" 404 None
2020-11-27 19:43:10,502 DEBUG service ping dependencies [ping:namekox_etcd.core.dependencies.etcd3.Etcd3Helper:etcd3] stopped
2020-11-27 19:43:10,503 DEBUG services ['ping'] stopped
2020-11-27 19:43:10,503 DEBUG killing services ['ping']
2020-11-27 19:43:10,503 DEBUG service ping already stopped
2020-11-27 19:43:10,503 DEBUG services ['ping'] killed
```
> curl http://127.0.0.1/api/assign/server/
```json
{
    "errs": "",
    "code": "Request:Success",
    "data": {
        "port": 80,
        "address": "127.0.0.1"
    },
    "call_id": "793a6279-44c0-4b55-9b82-aa0224fe5a8b"
}
```

# Debug
> config.yaml
```yaml
CONTEXT:
  - namekox_etcd.cli.subctx.etcd3:Etcd3
ETCD3:
  ping:
    host: 127.0.0.1
    port: 2379
WEBSERVER:
  host: 0.0.0.0
  port: 80
```
> namekox shell
```shell script
In [1]: nx.etcd3.proxy('ping').range('/namekox', prefix=True)
2020-11-27 19:49:47,550 DEBUG Starting new HTTP connection (1): 127.0.0.1:2379
2020-11-27 19:49:47,552 DEBUG http://127.0.0.1:2379 "GET /version HTTP/1.1" 200 45
2020-11-27 19:49:47,557 DEBUG Starting new HTTP connection (1): 127.0.0.1:2379
2020-11-27 19:49:47,558 DEBUG http://127.0.0.1:2379 "POST /v3/kv/range HTTP/1.1" 200 531
Out[1]: etcdserverpbRangeResponse(count=2, header=etcdserverpbResponseHeader(raft_term=13, cluster_id=14841639068965178418L, member_id=10276657743932975437L, revision=142), kvs=[mvccpbKeyValue(mod_revision=142, create_revision=142, value='{"port": 80, "address": "127.0.0.1"}', version=1, key='/namekox/ping.94375b42-9007-451b-b720-7e6550850fbe'), mvccpbKeyValue(mod_revision=141, create_revision=141, value='{"port": 80, "address": "127.0.0.1"}', version=1, key='/namekox/ping.94b56994-a652-41c0-97f3-32bc825befca')])
```
