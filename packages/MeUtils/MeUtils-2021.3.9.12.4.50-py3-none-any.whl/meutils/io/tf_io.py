#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : tf_io
# @Time         : 2021/2/26 4:19 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : https://www.jianshu.com/p/c2fabc8a6dad

# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MICTRZOO.
# @File         : io
# @Time         : 2021/2/26 11:09 上午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  :

import tensorflow as tf
from meutils.pipe import *
from meutils.path_utils import get_module_path

ZJY = 'hdfs://zjyprc-hadoop'
DATA = get_module_path("../../data", __file__)
_SUCCESS = f"{DATA}/_SUCCESS"


def tf_read(file, reader=pd.read_csv):
    """
    reader: lambda p: pd.read_csv(p, iterator=True, chunksize=10000)
    """
    with tf.io.gfile.GFile(file) as f:
        return reader(f)


def tf_write(df, file, **kwargs):
    with tf.io.gfile.GFile(file, 'w') as f:
        if isinstance(df, pd.DataFrame):
            df.to_csv(f, **kwargs)
        else:
            f.write(df)


# tf.io.gfile.remove
def tf_copy(pattern='/fds/infra-client/demo/x/*', output_dir=DATA):
    """复制文件夹下的文件到新文件夹"""
    if '*' not in pattern:  # 如果是个文件夹，默认匹配所有文件
        pattern += '/*'

    if pattern.startswith("/user/"):
        pattern = ZJY + pattern

    if output_dir.startswith("/user/"):
        output_dir = ZJY + output_dir

    if not tf.io.gfile.exists(output_dir):
        tf.io.gfile.makedirs(output_dir)

    files = tf.io.gfile.glob(pattern)
    logger.info(f"FILES:\n {files}")

    new_files = []
    for file in files:
        new_file = f"{output_dir}/{Path(file).name}"
        tf.io.gfile.copy(file, new_file, True)

        new_files.append(new_file)

    if output_dir.startswith('hdfs:'):
        tf.io.gfile.copy(_SUCCESS, output_dir, True)

    return new_files
