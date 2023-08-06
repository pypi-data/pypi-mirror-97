#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals


from namekox_ldap.constants import LDAP_CONFIG_KEY
from namekox_ldap.core.connection import LdapConnect
from namekox_core.core.friendly import AsLazyProperty
from namekox_core.core.service.dependency import Dependency


class LdapHelper(Dependency):
    def __init__(self, dbname, servers=None, retries=None, base_dn='', base_dc='', usrname='', usrpass='', options=None):
        self.dbname = dbname
        self._instance = None
        self.retries = retries
        self.base_dn = base_dn
        self.base_dc = base_dc
        self.usrname = usrname
        self.usrpass = usrpass
        self.servers = servers or []
        self.options = options or {}
        super(LdapHelper, self).__init__()

    @AsLazyProperty
    def configs(self):
        return self.container.config.get(LDAP_CONFIG_KEY, {})

    def setup(self):
        config = self.configs.get(self.dbname, {}).copy()
        'options' in config and config['options'].update(self.options)
        'servers' in config and config.update({'servers': self.servers or config['servers']})
        'base_dn' in config and config.update({'base_dn': self.base_dn or config['base_dn']})
        'base_dc' in config and config.update({'base_dc': self.base_dc or config['base_dc']})
        'usrname' in config and config.update({'usrname': self.usrname or config['usrname']})
        'usrpass' in config and config.update({'usrpass': self.usrname or config['usrpass']})
        'retries' in config and config.update({'retries': self.retries or config['retries']})
        self._instance = LdapConnect(config)

    def get_instance(self, context):
        return self._instance
