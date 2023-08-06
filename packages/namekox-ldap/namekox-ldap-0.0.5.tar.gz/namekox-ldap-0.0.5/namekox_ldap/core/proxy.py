#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals


from namekox_ldap.constants import LDAP_CONFIG_KEY
from namekox_core.core.friendly import AsLazyProperty


from .connection import LdapConnect


class LdapProxy(object):
    def __init__(self, config):
        self.config = config

    @AsLazyProperty
    def configs(self):
        return self.config.get(LDAP_CONFIG_KEY, {})

    def __call__(self, dbname):
        config = self.configs.get(dbname, {})
        return LdapConnect(config)
