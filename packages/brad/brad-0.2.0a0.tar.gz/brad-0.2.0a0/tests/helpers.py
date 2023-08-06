import numpy as np

RANDOM_10x5 = np.random.normal(size=(10, 5))
RANDOM_10x1 = np.random.sample(10)


def safe_mean(arr):
    if arr.size > 0:
        return arr.mean()
    return 0
