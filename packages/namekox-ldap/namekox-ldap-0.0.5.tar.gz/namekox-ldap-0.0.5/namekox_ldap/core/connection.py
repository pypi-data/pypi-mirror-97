#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals


import ldap3
import socket


from itertools import cycle
from ldap3.core.exceptions import LDAPException
from namekox_core.core.friendly import AsLazyProperty, ignore_exception, auto_sleep_retry
from namekox_ldap.constants import DEFAULT_LDAP_CONNECT_TIMEOUT, DEFAULT_LDAP_CONNECT_RETRIES


class LdapConnect(object):
    def __init__(self, config):
        self.config = config
        self._instance = None
        self._instance_excinfo = None

    @AsLazyProperty
    def options(self):
        return self.config.get('options', {})

    @AsLazyProperty
    def servers(self):
        servers = self.config.get('servers', [])
        return cycle(servers)

    @AsLazyProperty
    def base_dn(self):
        return self.config.get('base_dn', '')

    @AsLazyProperty
    def base_dc(self):
        return self.config.get('base_dc', '')

    @AsLazyProperty
    def usrname(self):
        return self.config.get('usrname', '')

    @AsLazyProperty
    def usrpass(self):
        return self.config.get('usrpass', '')

    @AsLazyProperty
    def retries(self):
        return self.config.get('retries', DEFAULT_LDAP_CONNECT_RETRIES)

    @staticmethod
    def _raise(exc_info):
        raise exc_info[1]

    @staticmethod
    def connect(servers, usrname, usrpass, base_dc, **options):
        config = servers.next()
        config.setdefault('connect_timeout', DEFAULT_LDAP_CONNECT_TIMEOUT)
        server = ldap3.Server(**config)
        server_user = '{0}\\{1}'.format(base_dc, usrname)
        if 'auto_bind' not in options:
            options.update({'auto_bind': True})
        if 'authentication' not in options:
            options.update({'authentication': ldap3.NTLM})
        return ldap3.Connection(server, user=server_user, password=usrpass, **options)

    def acquire(self):
        def check_available():
            self._instance_excinfo = None
            self._instance.extend.standard.who_am_i()

        def start_reconnect(exc_info):
            connection = self.connect(self.servers, self.usrname, self.usrpass, self.base_dc, **self.options)
            self._instance = connection

        def reset_reconnect(exc_info):
            self._instance = None
            self._instance_excinfo = exc_info
        expect_exception = (AttributeError, LDAPException, socket.error)
        start_reconnect = ignore_exception(start_reconnect, reset_reconnect)
        auto_sleep_retry(check_available, start_reconnect, expect_exception, max_retries=self.retries, time_sleep=0.001)
        self._instance_excinfo and self._raise(self._instance_excinfo)
        return self._instance
