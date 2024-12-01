from tools import *
import numpy as np


def task1():
    serial = 4455
    my, mx = np.meshgrid(np.arange(301), np.arange(301))
    vals = ((mx + 10) * my + serial) * (mx + 10)
    vals = (vals // 100) % 10 - 5
    best_sum = 0
    best_pos = None
    for y in range(1, 298):
        for x in range(1, 298):
            s = np.sum(vals[x: x + 3, y: y + 3])
            if s > best_sum:
                best_pos = x, y
                best_sum = s
    ic(best_pos, best_sum)


def task2():
    serial = 4455
    total = 300
    mx, my = np.meshgrid(np.arange(total + 1), np.arange(total + 1))
    vals = ((mx + 10) * my + serial) * (mx + 10)
    vals = (vals // 100) % 10 - 5
    sums = np.zeros((total + 1, total + 1), int)
    vals[:, 0] = 0
    vals[0, :] = 0
    for y in range(1, total + 1):
        for x in range(1, total + 1):
            sums[y, x] = sums[y - 1, x] + sums[y, x - 1] - sums[y - 1, x - 1] + vals[y, x]
    best_sum = 0
    best_pos = None
    for size in range(1, total):
        ic(size)
        for y in range(total - size):
            for x in range(total - size):
                s = sums[y + size, x + size] - sums[y, x + size] - sums[y + size, x] + sums[y, x]
                if s > best_sum:
                    best_pos = x + 1, y + 1, size
                    best_sum = s
    ic(best_pos, best_sum)
    x, y, s = best_pos
    ic(np.sum(vals[y: y + s, x: x + s]))
    # ic(np.sum(vals[269: 269 + 16, 90: 90 + 16]))
