from tools import *
import numpy as np
import pylab as plt


def load(fn: str):
    return np.array(list(get_int_lines(fn)))


def calc_task1(nodes: np.array, ry: int, rx: int):
    area = np.zeros((ry, rx), int)
    cursed = set()
    counts = {}
    for y in range(ry):
        for x in range(rx):
            p = np.abs(nodes - [x, y])
            p = p[:, 0] + p[:, 1]
            v = min(p)
            ndx = p[p == v]
            if len(ndx) > 1:
                area[y, x] = -1
            else:
                n = np.argmin(p)
                area[y, x] = n
                if n not in counts:
                    counts[n] = 0
                counts[n] += 1
                if y in (0, ry - 1) or x in (0, rx - 1):
                    cursed.add(n)
    # ic(area)
    for c in cursed:
        del counts[c]
    vals = [(v, k) for k, v in counts.items()]
    vals.sort()
    ic(vals)


def task1():
    nodes = load("i.txt")
    ic(nodes)
    ry = np.max(nodes[:, 0]) + 2
    rx = np.max(nodes[:, 1]) + 2
    ic(rx, ry)
    calc_task1(nodes, ry, rx)


def calc_task2(nodes: np.array, ry: int, rx: int):
    area = np.zeros((ry, rx), int)
    ret = 0
    for y in range(ry):
        for x in range(rx):
            p = np.abs(nodes - [x, y])
            p = p[:, 0] + p[:, 1]
            d = sum(p)
            area[y, x] = d
            if d < 10000:
                ret += 1
    ic(ret)
    plt.imshow(area < 10000)
    plt.show()


def task2():
    nodes = load("i.txt")
    ry = np.max(nodes[:, 0]) + 2
    rx = np.max(nodes[:, 1]) + 2
    calc_task2(nodes, ry, rx)
