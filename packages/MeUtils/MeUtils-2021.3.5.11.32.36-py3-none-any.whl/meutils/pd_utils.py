#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : pd_utils
# @Time         : 2020/11/12 11:35 上午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

from meutils.common import *


def duplicate_columns(frame):
    """keep='first' 
    https://stackoverflow.com/questions/14984119/python-pandas-remove-duplicate-columns/32961145#32961145
    数据大:
        dups = duplicate_columns(df)
        df.drop(dups, 1)

    数据小:
        df.T.drop_duplicates().T
    """
    frame = frame.fillna(-123456)  # 处理缺失值

    groups = frame.columns.to_series().groupby(frame.dtypes).groups
    dups = []
    for t, v in groups.items():
        dcols = frame[v].to_dict(orient="list")

        vs = list(dcols.values())
        ks = list(dcols.keys())
        lvs = len(vs)

        for i in range(lvs):
            for j in range(i + 1, lvs):
                if vs[i] == vs[j]:
                    dups.append(ks[j])  # keep='first'
                    break
    return dups


# reduce memory
def reduce_mem_usage(df):
    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    start_mem = df.memory_usage().sum() / 1024 ** 2
    for col in tqdm(df.columns, desc="Reduce memory"):
        col_type = df[col].dtypes
        if col_type in numerics:
            c_min = df[col].min()
            c_max = df[col].max()
            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)
            else:
                if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                    df[col] = df[col].astype(np.float16)
                elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)
        # else:
        #     df[col] = df[col].astype('category')

    end_mem = df.memory_usage().sum() / 1024 ** 2
    print('Memory usage after optimization is: {:.2f} MB'.format(end_mem))
    print('Decreased by {:.1f}%'.format(100 * (start_mem - end_mem) / start_mem))

    return df


def df2bhtml(df, title, subtitle=''):
    """to buidfull html"""
    msg = f"""
        <head>
            <meta charset="utf-8">
            <STYLE TYPE="text/css" MEDIA=screen>

                table.dataframe {{
                    border-collapse: collapse;
                    border: 2px solid #a19da2;
                    /*居中显示整个表格*/
                    margin: auto;
                }}

                table.dataframe thead {{
                    border: 2px solid #91c6e1;
                    background: #f1f1f1;
                    padding: 10px 10px 10px 10px;
                    color: #333333;
                }}

                table.dataframe tbody {{
                    border: 2px solid #91c6e1;
                    padding: 10px 10px 10px 10px;
                }}

                table.dataframe tr {{

                }}

                table.dataframe th {{
                    vertical-align: top;
                    font-size: 14px;
                    padding: 10px 10px 10px 10px;
                    color: #105de3;
                    font-family: arial;
                    text-align: center;
                }}

                table.dataframe td {{
                    text-align: center;
                    padding: 10px 10px 10px 10px;
                }}

                body {{
                    font-family: 宋体;
                }}

                h1 {{
                    color: #5db446
                }}

                div.header h2 {{
                    color: #0002e3;
                    font-family: 黑体;
                }}

                div.content h2 {{
                    text-align: center;
                    font-size: 28px;
                    text-shadow: 2px 2px 1px #de4040;
                    color: #fff;
                    font-weight: bold;
                    background-color: #008eb7;
                    line-height: 1.5;
                    margin: 20px 0;
                    box-shadow: 10px 10px 5px #888888;
                    border-radius: 5px;
                }}

                h3 {{
                    font-size: 22px;
                    background-color: rgba(0, 2, 227, 0.71);
                    text-shadow: 2px 2px 1px #de4040;
                    color: rgba(239, 241, 234, 0.99);
                    line-height: 1.5;
                }}

                h4 {{
                    color: #e10092;
                    font-family: 楷体;
                    font-size: 20px;
                    text-align: center;
                }}

                td img {{
                    /*width: 60px;*/
                    max-width: 300px;
                    max-height: 300px;
                }}

            </STYLE>
        </head>

            <body>

            <div align="center" class="header">
                <!--标题部分的信息-->
                <h1 align="center">{title}</h1>
                <h2 align="center">{subtitle}</h2>
            </div>

            <hr>

            <div class="content">
                <!--正文内容-->
                <h2> </h2>

                <div>
                    <h4></h4>
                    {df.to_html()}

            </div>

            <hr>

            <p style="text-align: center">

            </p>
            </body>
    """
    return msg





if __name__ == '__main__':
    df = pd.DataFrame([[1, 2, 3] * 10000, [2, 2, 3] * 10000, [3, 2, 3] * 10000])

    import time

    s = time.time()
    reduce_mem_usage(df)  # 34

    print(time.time() - s)
