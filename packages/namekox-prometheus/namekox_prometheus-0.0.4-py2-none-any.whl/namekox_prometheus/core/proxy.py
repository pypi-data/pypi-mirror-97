#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals


from namekox_core.core.friendly import AsLazyProperty
from namekox_prometheus.core.gateway import PrometheusGateway
from namekox_prometheus.constants import PROMETHEUS_CONFIG_KEY


class PrometheusProxy(object):
    def __init__(self, config, **options):
        self.config = config
        self.options = options

    @AsLazyProperty
    def configs(self):
        return self.config.get(PROMETHEUS_CONFIG_KEY, {})

    def __call__(self, dbname, **options):
        self.options.update(options)
        config = self.configs.get(dbname, {}).copy()
        config.update(self.options)
        return PrometheusGateway(**config)
