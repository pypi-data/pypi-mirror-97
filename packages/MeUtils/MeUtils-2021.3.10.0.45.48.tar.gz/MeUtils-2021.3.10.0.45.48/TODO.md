# 分组实现
```python
import itertools
import numpy as np
import pandas as pd

np.array_split(range(10), 3)

s = iter("123456789")
for x in itertools.islice(s, 2, 6):
    print(x)


df = pd.DataFrame(np.random.random((10000, 1000)))
np.array_split(df)


```