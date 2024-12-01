from tools import *
import numpy as np


def task1():
    limit = 110201
    limit += 10
    data = np.zeros((limit + 1,), int)
    data[:2] = [3, 7]
    pos = [0, 1]
    tail = 2
    while tail < limit:
        new = sum(data[pos])
        if new >= 10:
            data[tail] = new // 10
            data[tail + 1] = new % 10
            tail += 2
        else:
            data[tail] = new
            tail += 1
        for n in range(len(pos)):
            pos[n] = (pos[n] + data[pos[n]] + 1) % tail
    print("".join(map(str, data[limit-10:limit])))


def task2():
    limit = 100000000
    limit += 10
    data = np.zeros((limit + 1,), int)
    data[:2] = [3, 7]
    pos = [0, 1]
    tail = 2
    expect = 110201
    expect = list(map(int, str(expect)))
    expect = np.array(expect)
    while tail < limit:
        if tail % 10000 == 0:
            ic(pos, tail)
        new = sum(data[pos])
        both = False
        if new >= 10:
            data[tail] = new // 10
            data[tail + 1] = new % 10
            tail += 2
            both = True
        else:
            data[tail] = new
            tail += 1
        for n in range(len(pos)):
            pos[n] = (pos[n] + data[pos[n]] + 1) % tail
        if tail > len(expect) and np.all(expect == data[tail-len(expect): tail]):
            ic(tail - len(expect))
            return
        if tail > (len(expect) + 1) and np.all(expect == data[tail - len(expect) - 1: tail - 1]) and both:
            ic(tail - len(expect) - 1)
            return
