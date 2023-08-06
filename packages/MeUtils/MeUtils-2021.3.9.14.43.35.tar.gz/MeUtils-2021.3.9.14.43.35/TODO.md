# 分组实现
```python
import itertools
import numpy as np

np.array_split(range(10), 3)

s = iter("123456789")
for x in itertools.islice(s, 2, 6):
    print(x)
```