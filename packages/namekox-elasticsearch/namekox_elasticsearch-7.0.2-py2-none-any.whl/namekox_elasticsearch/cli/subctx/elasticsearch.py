#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals


from namekox_elasticsearch.core.proxy import ElasticSearchProxy


class ElasticSearch(object):
    def __init__(self, config):
        self.config = config
        self.proxy = ElasticSearchProxy(config)

    @classmethod
    def name(cls):
        return 'elasticsearch'
