#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals


class LoginFailed(Exception):
    pass


class PexpectError(Exception):
    pass


class ConnectError(Exception):
    pass


class MatchTimeout(Exception):
    pass
