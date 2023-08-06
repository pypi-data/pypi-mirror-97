# Install
```shell script
pip install -U namekox-prometheus
```

# Example
> ping.py
```python
#! -*- coding: utf-8 -*-

# author: forcemain@163.com
from __future__ import unicode_literals


from prometheus_client.registry import REGISTRY
from namekox_webserver.core.entrypoints.app import app
from namekox_prometheus.core.dependencies import PrometheusHelper


class Ping(object):
    name = 'ping'

    # https://github.com/prometheus/client_python
    prometheus = PrometheusHelper(name)

    @app.api('/metrics/send', methods=['POST'])
    def send_metrics(self, request):
        self.prometheus.push_gateway.send(registry=REGISTRY)

    @app.web('/metrics', methods=['GET'])
    def metrics(self, request):
        return self.prometheus.expose_metrics(request)
```

# Running
> config.yaml
```yaml
PROMETHEUS:
  ping:
    prefix: ~
    usrname: ~
    usrpass: ~
    gateway: 127.0.0.1:9091
    job: namekox
```
> namekox run ping
```shell script
2020-12-02 17:57:24,361 DEBUG load container class from namekox_core.core.service.container:ServiceContainer
2020-12-02 17:57:24,363 DEBUG starting services ['ping']
2020-12-02 17:57:24,363 DEBUG starting service ping entrypoints [ping:namekox_webserver.core.entrypoints.app.handler.WebServerHandler:metrics, ping:namekox_webserver.core.entrypoints.app.server.WebServer:server, ping:namekox_webserver.core.entrypoints.app.handler.ApiServerHandler:send_metrics]
2020-12-02 17:57:24,365 DEBUG spawn manage thread handle ping:namekox_webserver.core.entrypoints.app.server:handle_connect(args=(), kwargs={}, tid=handle_connect)
2020-12-02 17:57:24,366 DEBUG service ping entrypoints [ping:namekox_webserver.core.entrypoints.app.handler.WebServerHandler:metrics, ping:namekox_webserver.core.entrypoints.app.server.WebServer:server, ping:namekox_webserver.core.entrypoints.app.handler.ApiServerHandler:send_metrics] started
2020-12-02 17:57:24,366 DEBUG starting service ping dependencies [ping:namekox_prometheus.core.dependencies.PrometheusHelper:prometheus]
2020-12-02 17:57:24,366 DEBUG service ping dependencies [ping:namekox_prometheus.core.dependencies.PrometheusHelper:prometheus] started
2020-12-02 17:57:24,366 DEBUG services ['ping'] started
2020-12-02 17:57:27,530 DEBUG spawn manage thread handle ping:namekox_webserver.core.entrypoints.app.server:handle_request(args=(<eventlet.greenio.base.GreenSocket object at 0x10eed8550>, ('127.0.0.1', 50716)), kwargs={}, tid=handle_request)
2020-12-02 17:57:27,530 DEBUG spawn manage thread handle ping:namekox_webserver.core.entrypoints.app.server:handle_request(args=(<eventlet.greenio.base.GreenSocket object at 0x10eed8950>, ('127.0.0.1', 50717)), kwargs={}, tid=handle_request)
2020-12-02 17:57:27,540 DEBUG spawn worker thread handle ping:metrics(args=(<Request 'http://127.0.0.1/metrics' [GET]>,), kwargs={}, context={})
127.0.0.1 - - [02/Dec/2020 17:57:27] "GET /metrics HTTP/1.1" 200 483 0.002788
2020-12-02 17:57:29,898 DEBUG spawn worker thread handle ping:metrics(args=(<Request 'http://127.0.0.1/metrics' [GET]>,), kwargs={}, context={})
127.0.0.1 - - [02/Dec/2020 17:57:29] "GET /metrics HTTP/1.1" 200 3299 0.002194
```
> curl http://127.0.0.1/metrics
```shell script
# HELP python_info Python platform information
# TYPE python_info gauge
python_info{implementation="CPython",major="2",minor="7",patchlevel="16",version="2.7.16"} 1.0
# HELP request_total Total number of requests
# TYPE request_total counter
request_total{endpoint="/metrics",method="metrics",service="ping",status="succ",transport="WebServerHandler"} 1.0
# HELP request_created Total number of requests
# TYPE request_created gauge
request_created{endpoint="/metrics",method="metrics",service="ping",status="succ",transport="WebServerHandler"} 1.606903047541664e+09
# HELP request_latency Request duration in seconds
# TYPE request_latency histogram
request_latency_bucket{endpoint="/metrics",le="0.005",method="metrics",service="ping",status="succ",transport="WebServerHandler"} 1.0
request_latency_bucket{endpoint="/metrics",le="0.01",method="metrics",service="ping",status="succ",transport="WebServerHandler"} 1.0
request_latency_bucket{endpoint="/metrics",le="0.025",method="metrics",service="ping",status="succ",transport="WebServerHandler"} 1.0
request_latency_bucket{endpoint="/metrics",le="0.05",method="metrics",service="ping",status="succ",transport="WebServerHandler"} 1.0
request_latency_bucket{endpoint="/metrics",le="0.075",method="metrics",service="ping",status="succ",transport="WebServerHandler"} 1.0
request_latency_bucket{endpoint="/metrics",le="0.1",method="metrics",service="ping",status="succ",transport="WebServerHandler"} 1.0
request_latency_bucket{endpoint="/metrics",le="0.25",method="metrics",service="ping",status="succ",transport="WebServerHandler"} 1.0
request_latency_bucket{endpoint="/metrics",le="0.5",method="metrics",service="ping",status="succ",transport="WebServerHandler"} 1.0
request_latency_bucket{endpoint="/metrics",le="0.75",method="metrics",service="ping",status="succ",transport="WebServerHandler"} 1.0
request_latency_bucket{endpoint="/metrics",le="1.0",method="metrics",service="ping",status="succ",transport="WebServerHandler"} 1.0
request_latency_bucket{endpoint="/metrics",le="2.5",method="metrics",service="ping",status="succ",transport="WebServerHandler"} 1.0
request_latency_bucket{endpoint="/metrics",le="5.0",method="metrics",service="ping",status="succ",transport="WebServerHandler"} 1.0
request_latency_bucket{endpoint="/metrics",le="7.5",method="metrics",service="ping",status="succ",transport="WebServerHandler"} 1.0
request_latency_bucket{endpoint="/metrics",le="10.0",method="metrics",service="ping",status="succ",transport="WebServerHandler"} 1.0
request_latency_bucket{endpoint="/metrics",le="+Inf",method="metrics",service="ping",status="succ",transport="WebServerHandler"} 1.0
request_latency_count{endpoint="/metrics",method="metrics",service="ping",status="succ",transport="WebServerHandler"} 1.0
request_latency_sum{endpoint="/metrics",method="metrics",service="ping",status="succ",transport="WebServerHandler"} 0.00034809112548828125
# HELP request_latency_created Request duration in seconds
# TYPE request_latency_created gauge
request_latency_created{endpoint="/metrics",method="metrics",service="ping",status="succ",transport="WebServerHandler"} 1.60690304754172e+09
```
> curl -H "Content-Type: application/json" -X POST http://127.0.0.1/metrics/send
```json
{
    "errs": "", 
    "code": "Request:Success", 
    "data": null, 
    "call_id": "7436fc0b-6404-47dd-96fc-7c006a730d96"
}
```

# Debug
> config.yaml
```yaml
CONTEXT:
  - namekox_prometheus.cli.subctx.prometheus:Prometheus
PROMETHEUS:
  ping:
    prefix: ~
    usrname: ~
    usrpass: ~
    gateway: 127.0.0.1:9091
    job: namekox
```
> namekox shell
```shell script
Namekox Python 2.7.16 (default, Dec 13 2019, 18:00:32)
[GCC 4.2.1 Compatible Apple LLVM 11.0.0 (clang-1100.0.32.4) (-macos10.15-objc-s shell on darwin
In [1]: from prometheus_client import CollectorRegistry
In [2]: registry = CollectorRegistry()
In [3]: nx.prometheus.proxy('ping').send(registry=registry)
```
