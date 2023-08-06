#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals


from elasticsearch_dsl.connections import connections
from namekox_core.core.friendly import AsLazyProperty
from namekox_core.core.service.dependency import Dependency
from namekox_elasticsearch.constants import ELASTICSEARCH_CONFIG_KEY


class ElasticSearchHelper(Dependency):
    def __init__(self, dbname, **config):
        self.dbname = dbname
        self.config = config
        super(ElasticSearchHelper, self).__init__(dbname, **config)

    @AsLazyProperty
    def configs(self):
        return self.container.config.get(ELASTICSEARCH_CONFIG_KEY, {})

    def setup(self):
        config = self.configs.get(self.dbname, {}).copy()
        config.update(self.config)
        connections.create_connection(self.dbname, **config)

    def stop(self):
        return connections.remove_connection(self.dbname)
