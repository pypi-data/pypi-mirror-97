#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : functions
# @Time         : 2021/1/21 2:43 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

from typing import *
from meutils.pipe import *

# 布尔函数和简单计算
True and False
True or True


def add(x: Union[int, float], y: Union[int, float]):
    return x + y


def minus(x: Union[int, float], y: Union[int, float]):
    return x - y


def multiple(x: Union[int, float], y: Union[int, float]):
    return x * y


def divide(x: Union[int, float], y: Union[int, float]):
    return x / y


def double(x: Union[int, float, str]):
    return float(x)


def int64_t(x: Union[int, float]):
    return int(x)


def string(x: int):
    return str(x)


def round(x: float):
    return np.round(x)


def ceil(x: float):
    return np.ceil(x)


def floor(x: float):
    return np.floor(x)


# 字符串函数与工具类函数
split = str.split

str2time = time.strptime
size = len  # 字符串长度


def hour(x: int):  # 将毫秒时间戳转化为当前hour。
    return x / 1000 / 60 / 60


if __name__ == '__main__':
    print(int('0.1'))
