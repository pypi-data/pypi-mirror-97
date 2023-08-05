#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : get_dsl_conf
# @Time         : 2021/1/25 7:54 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.zk_utils import get_zk_config

data = get_zk_config('/mipush/dsl', mode='').strip()
data = [line.strip().split() for line in data.split('\r\n') if line != '' and not line.startswith('#')]

columns = ['fea_id', 'fea_name', 'component', 'fea_type', 'fea_dim', 'isOut', 'dnn_group']

df = pd.DataFrame(data, columns=columns)
df.dnn_group.astype(int).max()

### VeryGood!!!
df = pd.read_csv('dsl.txt', sep='\s+', names=columns, comment='#')

print(df.shape)
print(df.max())
