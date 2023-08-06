#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals


from namekox_prometheus.core.proxy import PrometheusProxy


class Prometheus(object):
    def __init__(self, config):
        self.config = config
        self.proxy = PrometheusProxy(config)

    @classmethod
    def name(cls):
        return 'prometheus'
