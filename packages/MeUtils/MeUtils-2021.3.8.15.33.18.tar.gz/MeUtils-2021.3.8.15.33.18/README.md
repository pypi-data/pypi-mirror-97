[![Downloads](http://pepy.tech/badge/meutils)](http://pepy.tech/project/meutils)

<h1 align = "center">:rocket: 常用工具类 :facepunch:</h1>

---

## Install
```bash
pip install -U meutils
```

## Usage
```python
from meutils.pipe import *

for i in range(5) | xtqdm:
    logger.info("这是一个进度条")

with timer('LOG'):
    logger.info("打印一条log所花费的时间")
```

---
## TODO
- add hook
- add zk/es/mongo/hdfs logger
- retry tenacity

pyspark https://wiki.n.miui.com/pages/viewpage.action?pageId=477643956

---
![git规范](https://tva1.sinaimg.cn/large/008eGmZEly1gn22tnx04dj312t0qpq6k.jpg)