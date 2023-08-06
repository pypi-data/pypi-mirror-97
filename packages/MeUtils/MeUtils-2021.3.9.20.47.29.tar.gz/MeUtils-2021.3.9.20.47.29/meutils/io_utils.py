#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : io_utils
# @Time         : 2020/11/19 3:04 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


from meutils.pipe import *


def to_hdf(df2name_list):
    with timer("to_hdf"):
        for df, name in df2name_list:
            df.to_hdf(name, 'w', complib='blosc', complevel=8)





