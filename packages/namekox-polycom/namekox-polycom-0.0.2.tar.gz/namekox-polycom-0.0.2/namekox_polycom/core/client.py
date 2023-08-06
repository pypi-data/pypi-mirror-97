#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals


import pexpect


from logging import getLogger
from pexpect.exceptions import EOF


from .. import constants, exceptions


logger = getLogger(__name__)


class PolycomClient(object):
    def __init__(self, host='127.0.0.1', port=22, username='admin', password='', **kwargs):
        self.inst = None

        self.host = host
        self.port = port
        self.username = username
        self.password = password

        self.timeout = kwargs.get('timeout', constants.DEFAULT_POLYCOM_TIMEOUT)
        self.logfile = kwargs.get('logfile', constants.DEFAULT_POLYCOM_LOGFILE)
        self.bshell_prompt = kwargs.get('bshell_prompt', constants.DEFAULT_POLYCOM_BSHELL_PROMPT)
        self.stdout_prompt = kwargs.get('stdout_prompt', constants.DEFAULT_POLYCOM_STDOUT_PROMPT)
        self.stdout_linsep = kwargs.get('stdout_linsep', constants.DEFAULT_POLYCOM_STDOUT_LINSEP)
        self.passwd_prompt = kwargs.get('passwd_prompt', constants.DEFAULT_POLYCOM_PASSWD_PROMPT)
        self.finger_prompt = kwargs.get('finger_prompt', constants.DEFAULT_POLYCOM_FINGER_PROMPT)

    def _raise(self, exc, msg=''):
        self.inst = None

        raise exc(msg) if msg else exc()

    def release(self):
        self.inst and self.inst.close(force=True)

    def connect(self):
        if self.inst is not None:
            return self.inst
        inst = pexpect.spawn('ssh {}@{} -p {}'.format(self.username, self.host, self.port))
        inst.logfile = self.logfile
        try:
            r = inst.expect([pexpect.TIMEOUT, self.finger_prompt, self.passwd_prompt], timeout=self.timeout)
        except EOF as e:
            logger.error(e.message)
            error = 'pexpect failed, child has exited'
            self._raise(exceptions.PexpectError, error)
        # match policy:
        #   0 - pexpect.TIMEOUT, not match
        #   1 - finger prompt
        #   2 - passwd prompt
        if r == 0:
            error = 'connect failed, wait finger|passwd prompt timeout({}s)'.format(self.timeout)
            self._raise(exceptions.ConnectError, error)
        if r == 1:
            inst.sendline('yes')
        if r == 2:
            inst.sendline(self.password)
        try:
            r = inst.expect([pexpect.TIMEOUT, self.stdout_linsep], timeout=self.timeout)
        except EOF as e:
            logger.error(e.message)
            error = 'pexpect failed, child has exited'
            self._raise(exceptions.PexpectError, error)
        if r == 0:
            error = 'matched failed, wait shell prompt timeout({}s)'.format(self.timeout)
            self._raise(exceptions.MatchTimeout, error)
        if r == 1:
            inst.sendline('')
        try:
            r = inst.expect([pexpect.TIMEOUT, self.bshell_prompt], timeout=self.timeout)
        except EOF as e:
            logger.error(e.message)
            error = 'pexpect failed, child has exited'
            self._raise(exceptions.PexpectError, error)
        if r == 0:
            error = 'matched failed, wait shell prompt timeout({}s)'.format(self.timeout)
            self._raise(exceptions.MatchTimeout, error)
        self.inst = inst
        return self.inst

    def execute(self, command, timeout=5):
        c = self.connect()
        c.sendline(command)
        c.sendline('')
        timeout = timeout or self.timeout
        r = c.expect([pexpect.TIMEOUT, self.bshell_prompt], timeout=timeout)
        error = 'matched failed, wait shell prompt timeout({}s)'.format(self.timeout)
        r == 0 and self._raise(exceptions.MatchTimeout, error)
        a = c.after.strip()
        b = c.before.replace(command, '', 1).strip()
        return {'before': b.split(self.stdout_linsep), 'after': a.split(self.stdout_linsep)}
