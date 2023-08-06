import numpy as np
from dms_influx.decorators import runtime


@runtime
def downsample_indexes(x, len_total):
    """Return downsampled indexes"""

    data = []
    chunk_len = round(len(x) / len_total * 2)
    chunk_start = 0
    chunk_end = chunk_len
    l = len_total // 2
    for i in range(l):
        if i + 1 == l:
            chunk_end = len(x)
        try:
            min_arg = np.argmin(x[chunk_start:chunk_end]) + chunk_start
        except ValueError:
            break
        max_arg = np.argmax(x[chunk_start:chunk_end]) + chunk_start
        data.append(min_arg)
        if min_arg != max_arg:
            data.append(max_arg)
        chunk_start += chunk_len
        chunk_end += chunk_len
    data.sort()
    return data
