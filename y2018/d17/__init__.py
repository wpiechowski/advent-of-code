from tools import *
import numpy as np
import pylab as plt
import sys


VAL_FREE = 0
VAL_FLOW = 4
VAL_RUN = 8
VAL_STATIC = 2
VAL_WALL = 10


def load(fn: str):
    x_range = [500, 500]
    y_range = [100, 0]
    data = np.zeros((2000, 2000), int)
    rx = r"([xy])=(\d+), [xy]=(\d+)..(\d+)"
    for axis, p0, p1, p2 in get_re_lines(fn, rx):
        p0, p1, p2 = map(int, (p0, p1, p2))
        p1, p2 = min_max((p1, p2))
        if axis == "x":
            x_range[0] = min(p0, x_range[0])
            x_range[1] = max(p0, x_range[1])
            y_range[0] = min(y_range[0], p1)
            y_range[1] = max(y_range[1], p2)
            data[p1: p2 + 1, p0] = VAL_WALL
        else:
            x_range[0] = min(x_range[0], p1)
            x_range[1] = max(x_range[1], p2)
            y_range[0] = min(y_range[0], p0)
            y_range[1] = max(y_range[1], p0)
            data[p0, p1: p2 + 1] = VAL_WALL
    # return data[y_range[0]: y_range[1] + 1, x_range[0] - 100: x_range[1] + 100], 500 - x_range[0] + 1
    return data[y_range[0]: y_range[1] + 1, : x_range[1] + 100], 500


# 0 - ground, 1 - blocked
def fall(data: np.array, y: int, x: int, dx: int, plot_fun: callable) -> bool:
    if y == data.shape[0]:
        return False
    if data[y, x] in (VAL_WALL, VAL_STATIC, VAL_RUN):
        return data[y, x] != VAL_RUN
    data[y, x] = VAL_FLOW
    ret = fall(data, y + 1, x, 0, plot_fun)
    if ret:
        left = right = True
        if dx != 1:
            left &= fall(data, y, x - 1, -1, plot_fun)
        if dx != -1:
            right &= fall(data, y, x + 1, 1, plot_fun)
        ret = left and right
        if not ret:
            for dx in (-1, 1):
                xx = x
                while data[y, xx] in (VAL_FLOW, VAL_STATIC, VAL_RUN):
                    data[y, xx] = VAL_RUN
                    xx -= dx
    if ret:
        if data[y, x] != VAL_RUN:
            data[y, x] = VAL_STATIC
        if dx == 0:
            plot_fun(data)
    else:
        data[y, x] = VAL_RUN
    return ret


def task1():
    sys.setrecursionlimit(100000)
    data, x0 = load("i.txt")
    ic(x0)
    plt.ion()
    fig, ax = plt.subplots(layout="tight")
    # data[0, :3] = [1, 2, 3]
    # data = data[:50, :]
    plot_data = plt.imshow(data, interpolation="nearest")
    # data[0, :3] = 0
    last_t = time.time()

    def plot_fun(d: np.array):
        nonlocal last_t
        now = time.time()
        if now - last_t > 1:
            last_t = now
            plot_data.set_data(d)
            plt.draw()
        fig.canvas.flush_events()

    fall(data, 0, x0, 0, plot_fun)
    ic("done")
    ret = np.sum(data == VAL_RUN) + np.sum(data == VAL_STATIC) + np.sum(data == VAL_FLOW)
    ic(ret)
    ret = np.sum(data == VAL_STATIC)
    ic(ret)
    plot_fun(data)
    plt.ioff()
    plt.show()
