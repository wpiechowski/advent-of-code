import numpy as np


def process(vals: np.array) -> int:
    print(vals)
    if np.all(vals==0):
        return 0
    else:
        v = process(np.diff(vals))
        return v + vals[-1]


def task1():
    ret = 0
    for line in open("i09a.txt"):
        vals = np.fromiter(map(int, line.strip().split(" ")), dtype=int)
        ret += process(vals[::-1])
    print(ret)
