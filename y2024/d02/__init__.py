from tools import *
import numpy as np


def task1():
    fn = "i.txt"
    goods = 0
    for line in get_int_lines(fn):
        d = np.diff(line)
        if np.all(d > 0) and np.all(d <= 3):
            goods += 1
        if np.all(d < 0) and np.all(d >= -3):
            goods += 1
    print(goods)


def is_good(vals):
    for k in range(len(vals)):
        v2 = vals[:k] + vals[k+1:]
        d = np.diff(v2)
        if np.all(d > 0) and np.all(d <= 3):
            return True
        if np.all(d < 0) and np.all(d >= -3):
            return True
    return False


def task2():
    fn = "i.txt"
    goods = 0
    for line in get_int_lines(fn):
        if is_good(line):
            goods += 1
    print(goods)
