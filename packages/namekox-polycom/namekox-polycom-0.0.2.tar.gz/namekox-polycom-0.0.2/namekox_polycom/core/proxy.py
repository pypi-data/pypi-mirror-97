#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals


from .connection import connections


class PolycomProxy(object):
    def __init__(self, config):
        self.config = config

    def __call__(self, alias, **options):
        config = self.config.copy()
        config.update(options)
        return connections.add_conn(alias, **config)
