#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals


from elasticsearch_dsl.connections import connections
from namekox_core.core.friendly import AsLazyProperty
from namekox_elasticsearch.constants import ELASTICSEARCH_CONFIG_KEY


class ElasticSearchProxy(object):
    def __init__(self, config, **options):
        self.dbname = 'default'
        self.config = config
        self.options = options

    @AsLazyProperty
    def configs(self):
        return self.config.get(ELASTICSEARCH_CONFIG_KEY, {})

    def __call__(self, dbname, **options):
        self.dbname = dbname
        self.options.update(options)
        config = self.configs.get(dbname, {}).copy()
        config.update(self.options)
        connections.create_connection(dbname, **config)
        return self
