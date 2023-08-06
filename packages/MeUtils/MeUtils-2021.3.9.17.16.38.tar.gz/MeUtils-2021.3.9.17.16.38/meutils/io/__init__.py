#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : __init__.py
# @Time         : 2021/2/26 4:19 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *


def to_excel(df2name_list, to_excel_kwargs=None):
    if to_excel_kwargs is None:
        to_excel_kwargs = {}

    with timer("to_excel"):
        with pd.ExcelWriter('filename.xlsx') as writer:
            for df, sheet_name in df2name_list:
                df.to_excel(writer, sheet_name, **to_excel_kwargs)
