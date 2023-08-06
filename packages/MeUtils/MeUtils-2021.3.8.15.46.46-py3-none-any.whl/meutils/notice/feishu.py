#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : feishu
# @Time         : 2021/1/20 6:04 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


from meutils.pipe import *
from meutils.zk_utils import get_zk_config


def send_feishu(body, hook_url=get_zk_config('/mipush/bot')['ann']):
    """

    :param body: {"title": "x", "text": "xx"}
    :param hook_url:
    :return:
    """
    logger.info(body)
    return requests.post(hook_url, json=body).json()


if __name__ == '__main__':
    # from meutils.pd_utils import better_df2html
    send_feishu({"title": "NoticeTest", "text": '...', "msg_type": "html"})
    # todo：
    #   1. 支持富文本，集成miwork
    #   2. 回调


