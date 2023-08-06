#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals


from .client import PolycomClient


class Connections(object):
    def __init__(self):
        self._conn = {}

    def add_conn(self, alias, **config):
        self._conn[alias] = PolycomClient(**config) if alias not in self._conn else self._conn[alias]
        return self._conn[alias]

    def get_conn(self, alias):
        return self._conn[alias]

    def del_conn(self, alias):
        conn = self._conn.pop(alias, None)
        conn is not None and conn.release()

    def release(self):
        [self.del_conn(alias) for alias in self._conn.keys()]


connections = Connections()
