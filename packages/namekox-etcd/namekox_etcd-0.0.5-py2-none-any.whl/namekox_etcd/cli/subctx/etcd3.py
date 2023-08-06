#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals


from namekox_etcd.core.proxy import Etcd3Proxy


class Etcd3(object):
    def __init__(self, config):
        self.config = config
        self.proxy = Etcd3Proxy(config)

    @classmethod
    def name(cls):
        return 'etcd3'
