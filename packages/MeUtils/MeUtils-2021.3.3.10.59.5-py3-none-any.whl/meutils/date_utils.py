#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : date_utils
# @Time         : 2020/11/12 11:41 上午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

from meutils.common import *

"""
pd.to_datetime(time.time(), unit='s')
>>> f'{now:%Y-%m-%d %H:%M:%S}'

"""


def date_difference(fmt='%Y-%m-%d %H:%M:%S', start_date: Any = datetime.datetime.now(), **kwargs) -> str:
    """
    start_date: datetime.datetime.today()
    days: float = ...,
    seconds: float = ...,
    microseconds: float = ...,
    milliseconds: float = ...,
    minutes: float = ...,
    hours: float = ...,
    weeks
    """
    if isinstance(start_date, (str, int)):
        start_date = datetime.datetime.strptime(str(start_date), fmt)
    date = start_date - datetime.timedelta(**kwargs)
    return date.strftime(fmt)


if __name__ == '__main__':
    print(date_difference(days=1))
    print(date_difference('%Y%m%d', days=1))
    print(date_difference('%Y%m%d', start_date=20210222, days=1))
    print(date_difference('%Y%m%d', days=2))

