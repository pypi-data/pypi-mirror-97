#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : zk
# @Time         : 2021/2/7 9:43 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.zk_utils import *

zk_watcher('/mipush/log')

if __name__ == '__main__':
    while 1:
        time.sleep(10)
        print(ZKConfig.info)


