#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals


from namekox_polycom.core.proxy import PolycomProxy


class Polycom(object):
    def __init__(self, config):
        self.config = config
        self.proxy = PolycomProxy(config)

    @classmethod
    def name(cls):
        return 'polycom'
