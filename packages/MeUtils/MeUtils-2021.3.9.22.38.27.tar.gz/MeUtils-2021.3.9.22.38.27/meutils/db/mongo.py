#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : Python.
# @File         : mimongo
# @Time         : 2020-03-20 11:26
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :
# https://www.jb51.net/article/159652.htm
# https://www.cnblogs.com/kaituorensheng/p/5181410.html

from meutils.pipe import *
from meutils.decorators import Singleton
from pymongo import MongoClient


class DBConf(BaseConfig):
    database: str
    user: str
    passwd: str
    ips: str
    replicaSet: str


@Singleton
class Mongo(object):

    def __init__(self, db='mig3_algo_push', url="mongodb://localhost:27017"):
        """
        :param db:
        :param print_info:
        """
        if url is None:
            conf = DBConf.parse_zk('/mipush/db/mongodb')
            url = f"mongodb://{conf.user}:{conf.passwd}@{conf.ips}/{conf.database}?replicaSet={conf.replicaSet}&authSource=admin"

        self.client = MongoClient(url)
        self.db = self.client[db]

        self.client_info = {
            "主节点": self.client.is_primary,
            "最大连接数": self.client.max_pool_size,
            'self.client.admin.command': self.client.admin.command('ismaster')
        }


if __name__ == '__main__':
    Mongo(url=None)
