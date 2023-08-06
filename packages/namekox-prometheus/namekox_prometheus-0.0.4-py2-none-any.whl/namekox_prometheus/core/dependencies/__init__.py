#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals


import time


from werkzeug.wrappers import Response
from prometheus_client.registry import REGISTRY
from namekox_core.core.friendly import AsLazyProperty
from prometheus_client.exposition import choose_encoder
from prometheus_client.metrics import Counter, Histogram
from namekox_core.core.service.dependency import Dependency
from namekox_prometheus.core.gateway import PrometheusGateway
from namekox_prometheus.constants import PROMETHEUS_CONFIG_KEY


class PrometheusHelper(Dependency):
    def __init__(self, dbname, **push_options):
        self.dbname = dbname
        self.perf_counter = {}
        self.push_gateway = None
        self.push_options = push_options

        self.request_total_counter = None
        self.request_latency_histogram = None

        super(PrometheusHelper, self).__init__(dbname, **push_options)

    @AsLazyProperty
    def configs(self):
        return self.container.config.get(PROMETHEUS_CONFIG_KEY, {})

    def setup_gateway(self, options):
        self.push_gateway = PrometheusGateway(**options)

    def setup_metrics(self, context, status='succ'):
        finish_time = time.time()
        called_time = self.perf_counter.pop(id(context), 0)
        duration = finish_time - called_time
        method = context.entrypoint.obj_name
        transport = context.entrypoint.__class__.__name__
        service = context.service.name
        endpoint = getattr(context.entrypoint, 'rule', '')
        called_time and self.request_total_counter.labels(transport, service, endpoint, method, status).inc()
        called_time and self.request_latency_histogram.labels(transport, service, endpoint, method, status).observe(duration)

    def setup(self):
        config = self.configs.get(self.dbname, {}).copy()
        config.update(self.push_options)
        prefix = config.pop('prefix', None)
        self.setup_gateway(config)
        request_total_counter_name = '{}_request_total'.format(prefix) if prefix else 'request_total'
        self.request_total_counter = Counter(
            request_total_counter_name,
            'Total number of requests',
            ['transport', 'service', 'endpoint', 'method', 'status']
        )
        request_latency_histogram_name = '{}_request_latency'.format(prefix) if prefix else 'request_latency'
        self.request_latency_histogram = Histogram(
            request_latency_histogram_name,
            'Request duration in seconds',
            ['transport', 'service', 'endpoint', 'method', 'status']
        )

    @staticmethod
    def expose_metrics(request):
        metrics_names = request.args.getlist('name', [])
        registry = REGISTRY.restricted_registry(metrics_names) if metrics_names else REGISTRY
        encoder, content_type = choose_encoder(request.headers['Accept'])
        results = encoder(registry)
        return Response(results, content_type=content_type)

    def worker_setup(self, context):
        self.perf_counter[id(context)] = time.time()

    def worker_result(self, context, result=None, exc_info=None):
        self.setup_metrics(context, status='succ')

    def worker_teardown(self, context):
        self.setup_metrics(context, status='fail')
