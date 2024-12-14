import time

from tools import *
import numpy as np
import pylab as plt


@dataclass
class Robot:
    x: int
    y: int
    dx: int
    dy: int


def load_iter(fn: str):
    for vals in get_int_lines(fn):
        yield Robot(*vals)


def task1():
    # task = (7, 11, "i1.txt", 100)
    task = (103, 101, "i.txt", 100)
    sy, sx, fn, steps = task
    hy = sy // 2
    hx = sx // 2
    quarters = [0] * 4
    for r in load_iter(fn):
        ny = (r.y + steps * r.dy) % sy
        nx = (r.x + steps * r.dx) % sx
        ic(r, nx, ny)
        if ny == hy or nx == hx:
            continue
        q = 0
        if ny > hy:
            q += 1
        if nx > hx:
            q += 2
        quarters[q] += 1
    print(quarters, quarters[0] * quarters[1] * quarters[2] * quarters[3])


def map_robots(robots, arr):
    arr[:, :] = 0
    for r in robots:
        arr[r.y, r.x] = 1


def task2():
    task = (103, 101, "i.txt", 100)
    sy, sx, fn, steps = task
    robots = list(load_iter(fn))
    arr = np.zeros((sy, sx), dtype=int)
    map_robots(robots, arr)
    plt.ion()
    fig, ax = plt.subplots()
    im = ax.imshow(arr)
    fig.canvas.flush_events()
    # plt.show(block=False)
    best = 0
    for i in range(10000000):
        print(i)
        for r in robots:
            r.x = (r.x + r.dx) % sx
            r.y = (r.y + r.dy) % sy
        map_robots(robots, arr)
        s = np.sum(arr)
        if s < best:
            continue
        best = s
        ax.clear()
        ax.imshow(arr)
        ax.set_title(str(i+1))
        plt.draw()
        fig.canvas.flush_events()
        time.sleep(1)
