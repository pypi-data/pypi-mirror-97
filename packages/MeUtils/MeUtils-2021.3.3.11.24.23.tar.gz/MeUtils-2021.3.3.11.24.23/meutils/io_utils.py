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



def tf_read_text(
        tf,
        file='/user/h_data_platform/platform/browser/content_daily/date=20201117/000000_0',
        prefix='hdfs://zjyprc-hadoop'
):
    """
        for i in data:
            i.numpy().decode().split('\t')
    :param tf:
    :param file:
    :param prefix:
    :return:
    """
    pattern = prefix + file
    fs = tf.data.Dataset.list_files(file_pattern=pattern)
    # ds = tf.data.TFRecordDataset(filenames=fs)
    data = tf.data.TextLineDataset(fs)
    return data

