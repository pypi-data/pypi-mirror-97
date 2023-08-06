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
from meutils.path_utils import get_module_path

HDFS = 'hdfs://zjyprc-hadoop'
DATA = get_module_path("../data", __file__)
_SUCCESS = f"{DATA}/_SUCCESS"


def _process_success(output_dir):
    if output_dir.startswith('hdfs:') and tf.io.gfile.isdir(output_dir):
        tf.io.gfile.copy(_SUCCESS, output_dir, True)


def _process_hdfs_path(p):
    if p.startswith('/user/'):
        p = HDFS + p
    return p


def _process_pattern(pattern):
    pattern = _process_hdfs_path(pattern)

    if tf.io.gfile.isdir(pattern):  # 如果是个文件夹，默认匹配所有文件
        pattern += '/*'
    return pattern


def rm(path):
    path = _process_hdfs_path(path)

    if tf.io.gfile.isdir(path):
        tf.io.gfile.rmtree(path)
    elif tf.io.gfile.exists(path):  # 文件夹也返回 True
        tf.io.gfile.remove(path)


def cp(pattern, output_dir=DATA):
    """复制文件夹下的文件到新文件夹"""
    pattern = _process_pattern(pattern)
    output_dir = _process_hdfs_path(output_dir)

    if not tf.io.gfile.exists(output_dir):
        tf.io.gfile.makedirs(output_dir)

    files = tf.io.gfile.glob(pattern)

    logger.info("FILES:\n {}".format('\t' + '\n\t'.join(files)))

    new_files = []
    for file in files:
        new_file = f"{output_dir}/{Path(file).name}"
        tf.io.gfile.copy(file, new_file, True)

        new_files.append(new_file)

    return new_files


def df2write(df, file, index=False, **kwargs):
    """仅支持单文件
    df.to_csv(f, index=False, header=False)
    """
    file = _process_hdfs_path(file)

    with tf.io.gfile.GFile(file, 'w') as f:
        df.to_csv(f, index=index, **kwargs)


def read2df(file, **kwargs):
    """仅支持单文件
    pd.read_csv(p, iterator=True, chunksize=10000)
    """
    file = _process_hdfs_path(file)

    with tf.io.gfile.GFile(file, 'rb') as f:
        return pd.read_csv(f, **kwargs)


def read2dataset(pattern, format='TextLineDataset'):
    """支持多文件大数据

    :param pattern:
    :param format: 'TextLineDataset', 'TFRecordDataset'
    :return:
        for i in ds:
            i.numpy().decode().split('\t')
    """
    pattern = _process_pattern(pattern)

    fs = tf.data.Dataset.list_files(file_pattern=pattern)
    ds = tf.data.__getattribute__(format)(fs)
    return ds
