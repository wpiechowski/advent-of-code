from tools import *
import numpy as np


def load():
    fn = "i.txt"
    items = list(get_int_lines(fn))
    return items


def task1():
    items = load()
    a = np.zeros((1000, 1000), int)
    for _, x0, y0, dx, dy in items:
        a[y0: y0 + dy, x0: x0 + dx] += 1
    ic(np.sum(a > 1))


def task2():
    items = load()
    for i1 in items:
        for i2 in items:
            if i1 is i2:
                continue
            oo = True
            for d in (0, 1):
                p0 = max(i1[1 + d], i2[1 + d])
                p1 = min(i1[1 + d] + i1[3 + d], i2[1 + d] + i2[3 + d])
                if p0 >= p1:
                    oo = False
            if oo:
                break
        else:
            ic(i1)
