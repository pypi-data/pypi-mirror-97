#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals


from namekox_etcd.core.client import Etcd3Client
from namekox_etcd.constants import ETCD3_CONFIG_KEY
from namekox_core.core.friendly import AsLazyProperty


class Etcd3Proxy(object):
    def __init__(self, config, **options):
        self.config = config
        self.options = options

    @AsLazyProperty
    def configs(self):
        return self.config.get(ETCD3_CONFIG_KEY, {})

    def __call__(self, dbname, **options):
        self.options.update(options)
        config = self.configs.get(dbname, {})
        config.update(self.options)
        return Etcd3Client(**config)
