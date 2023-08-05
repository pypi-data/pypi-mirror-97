#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : tf_io
# @Time         : 2021/2/26 4:19 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : https://www.jianshu.com/p/c2fabc8a6dad


import tensorflow as tf
from meutils.pipe import *


def tf_read(file, reader=None):
    """TODO：待支持大数据
    reader: pd.read_csv
    """
    with tf.io.gfile.GFile(file) as f:
        if reader is not None:
            return reader(f)
        else:
            return f.read()


def tf_write(file, file_content):
    with tf.io.gfile.GFile(file, 'w') as f:
        if isinstance(file_content, pd.DataFrame):
            file_content.to_csv(f)
        else:
            f.write(file_content)


def tf_copy_dir(pattern='/fds/infra-client/demo/x/*', output_dir='/fds/infra-client/output'):
    """复制文件夹下的文件到新文件夹"""
    files = tf.io.gfile.glob(pattern)
    logger.info(f"FILES: {files}")

    for file in files:
        if not tf.io.gfile.exists(output_dir):
            tf.io.gfile.makedirs(output_dir)

        tf.io.gfile.copy(file, f"{output_dir}/{Path(file).name}", True)
    return [Path(i).name for i in files]
