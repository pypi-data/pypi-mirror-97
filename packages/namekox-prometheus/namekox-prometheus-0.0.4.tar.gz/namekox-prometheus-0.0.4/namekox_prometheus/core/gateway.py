#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals


from functools import partial
from prometheus_client.exposition import basic_auth_handler, push_to_gateway


class PrometheusGateway(object):
    def __init__(self, **options):
        self.options = options

    def send(self, **options):
        self.options.update(options)
        config = self.options.copy()
        prefix = config.pop('prefix', None)
        u_name = config.pop('usrname', None)
        u_pass = config.pop('usrpass', None)
        config.setdefault('handler', partial(basic_auth_handler, username=u_name, password=u_pass))
        return push_to_gateway(**config)
