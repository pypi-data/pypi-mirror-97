#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : common
# @Time         : 2020/11/12 11:42 上午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 单向引用，避免循环引用


import os
import gc
import re
import sys
import time

import joblib
import datetime
import pickle
import operator
import inspect
import requests
import resource
import socket
import warnings
import argparse
import yaml
import fire
import itertools
import subprocess
import wrapt
import multiprocessing

import numpy as np
import pandas as pd

from typing import *
from PIL import Image
from pathlib import Path
from tqdm.auto import tqdm
from contextlib import contextmanager
from functools import reduce, lru_cache
from collections import Counter, OrderedDict
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from pydantic import BaseModel, Field

# ME
from meutils.log_utils import logger
from meutils.models import BaseConfig

from meutils.crontab import CronTab
from meutils.besttable import Besttable

try:
    import simplejson as json
except ImportError:
    import json

warnings.filterwarnings("ignore")
tqdm.pandas()

# 常量
START_TIME = time.time()
CPU_NUM = multiprocessing.cpu_count()
HOST_NAME = socket.getfqdn(socket.gethostname())
LOCAL_HOST = socket.gethostbyname(HOST_NAME)

# json: dict -> str
bjson = lambda d: json.dumps(d, indent=4, ensure_ascii=False)

# args
get_args = lambda func: inspect.getfullargspec(func).args


# run time
@contextmanager
def timer(task="timer"):
    """https://www.kaggle.com/lopuhin/mercari-golf-0-3875-cv-in-75-loc-1900-s
        with timer() as t:
            time.sleep(3)
    """

    logger.info(f"{task} started")
    s = time.time()
    yield
    e = time.time()
    logger.info(f"{task} done in {e - s:.3f} s")


# limit memory
def limit_memory(memory=16):
    """
    :param memory: 默认限制内存为 16G
    :return:
    """
    rsrc = resource.RLIMIT_AS
    # res_mem=os.environ["RESOURCE_MEM"]
    memlimit = memory * 1024 ** 3
    resource.setrlimit(rsrc, (memlimit, memlimit))
    # soft, hard = resource.getrlimit(rsrc)
    logger.info("memory limit as: %s G" % memory)


def magic_cmd(cmd='ls', parse_fn=lambda s: s, print_output=False):
    """

    :param cmd:
    :param parse_fn: lambda s: s.split('\n')
    :param r_output:
    :return:
    """
    cmd = ' '.join(cmd.split())
    status, output = subprocess.getstatusoutput(cmd)
    output = output.strip()

    logger.info(f"CMD: {cmd}")
    logger.info(f"CMD Status: {status}")

    if print_output:
        logger.info(f"CMD Output: {output}")

    return status, parse_fn(output)


def download(url, rename=None):
    cmd = f"wget {url}"
    if rename:
        cmd += f" -O {rename}"

    os.system(cmd)


def yaml_load(path):
    """opener(yaml.load)"""
    with open(path) as f:
        return yaml.load(f)


def dict2yaml(dic, file=None):
    s = yaml.dump(dic)
    print(s)

    if file:
        with open(file, 'w') as f:
            f.write(s)


def git_pull(repo='dsl3'):
    repo_name = repo.split('/')[-1][:-4]
    if Path(repo_name).exists():
        magic_cmd(f'cd {repo_name} && git pull')
    else:
        magic_cmd(f'git clone {repo}')


if __name__ == '__main__':
    with timer() as t:
        time.sleep(3)

    status, output = magic_cmd('ls')
    print(status, output)

    d = {'a': 1, 'b': 2}
    print(bjson(d))
    print(BaseConfig.parse_obj(d))
