#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals


from namekox_core.core.friendly import AsLazyProperty
from namekox_polycom.constants import POLYCOM_CONFIG_KEY
from namekox_polycom.core.connection import connections
from namekox_core.core.service.dependency import Dependency


class PolycomHelper(Dependency):
    def __init__(self, **options):
        self.options = options
        super(PolycomHelper, self).__init__(**options)

    @AsLazyProperty
    def config(self):
        return self.container.config.get(POLYCOM_CONFIG_KEY, {})

    def stop(self):
        connections.release()

    def add_conn(self, alias, **options):
        config = self.config.copy()
        config.update(self.config)
        config.update(options)
        return connections.add_conn(alias, **config)

    def get_conn(self, alias):
        return connections.get_conn(alias)

    def del_conn(self, alias):
        return connections.del_conn(alias)

    def cmd_exec(self, alias, command, timeout=5):
        client = self.get_conn(alias)
        return client.execute(command, timeout)
