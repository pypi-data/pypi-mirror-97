#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals


import six
import json
import socket


from namekox_etcd.constants import ETCD3_CONFIG_KEY
from namekox_core.core.generator import generator_uuid
from namekox_core.core.service.dependency import Dependency
from namekox_etcd.core.client import Etcd3Client, Etcd3EventType
from namekox_core.core.friendly import AsLazyProperty, ignore_exception


class Etcd3Helper(Dependency):
    def __init__(self, dbname, serverid=None, leasettl=None, watching=None, allotter=None, coptions=None, roptions=None):
        self.services = {}
        self.instance = None
        self.dbname = dbname
        self.watchobj = None
        self.leaseobj = None
        self.lease_gt = None
        self.watching = watching
        self.allotter = allotter
        self.leasettl = leasettl or 5
        self.coptions = coptions or {}
        self.roptions = roptions or {}
        self.serverid = serverid or generator_uuid()
        super(Etcd3Helper, self).__init__(dbname, serverid, leasettl, watching, allotter, coptions, roptions)

    @AsLazyProperty
    def configs(self):
        return self.container.config.get(ETCD3_CONFIG_KEY, {})

    @staticmethod
    def get_host_byname():
        name = socket.gethostname()
        return ignore_exception(socket.gethostbyname)(name)

    def get_serv_name(self, name):
        return name.rsplit('/', 1)[-1].split('.', 1)[0]

    def gen_serv_name(self, name):
        return '{}/{}.{}'.format(self.watching, name, self.serverid)

    def setup_leaseobj(self):
        self.leaseobj = self.instance.Lease(self.leasettl)
        self.leaseobj.keepalive()

    def update_etcd_services(self, e):
        if not self.services:
            services = {}
            for s in self.instance.range(self.watching, prefix=True).kvs:
                name = self.get_serv_name(s.key)
                data = ignore_exception(json.loads)(s.value)
                data and services.setdefault(name, [])
                data and (data not in services[name]) and services[name].append(data)
            self.services = services
        elif e.type == Etcd3EventType.DELETE:
            name = self.get_serv_name(e.key)
            data = ignore_exception(json.loads)(e.value)
            data and (data in self.services[name]) and self.services[name].remove(data)
        elif e.type == Etcd3EventType.PUT:
            name = self.get_serv_name(e.key)
            data = ignore_exception(json.loads)(e.value)
            data and self.services.setdefault(name, [])
            data and (data not in self.services[name]) and self.services[name].append(data)
        self.allotter and self.allotter.set(self)

    def setup_watching(self):
        self.watchobj = self.instance.Watcher(key=self.watching, prefix=True, progress_notify=True)
        self.watchobj.onEvent('.*', self.update_etcd_services)
        self.watchobj.runDaemon()

    def setup_register(self):
        r_options = self.roptions.copy()
        host_addr = self.get_host_byname()
        serv_name = self.gen_serv_name(self.container.service_cls.name)
        r_options.setdefault('port', 80)
        r_options.setdefault('address', host_addr or '127.0.0.1')
        host_info = json.dumps(r_options)
        self.instance.put(serv_name, host_info)

    def setup_allotter(self):
        self.allotter.set(self)

    def setup(self):
        config = self.configs.get(self.dbname, {}).copy()
        [config.update({k: v}) for k, v in six.iteritems(self.coptions)]
        self.instance = Etcd3Client(**config)
        self.coptions = config

    def start(self):
        self.leasettl and self.setup_leaseobj()
        self.watching and self.setup_watching()
        self.watching and self.setup_register()
        self.allotter and self.setup_allotter()

    def stop(self):
        self.watchobj and self.watchobj.stop()
        self.leaseobj and self.leaseobj.cancel_keepalive()
        self.leaseobj and ignore_exception(self.leaseobj.revoke)()
        self.instance and ignore_exception(self.instance.close)()
