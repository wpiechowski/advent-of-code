import time

from tools import *
import numpy as np
import pylab as plt


def load(fn: str):
    pos = []
    vel = []
    for p1, p2, v1, v2 in get_int_lines(fn):
        pos.append([p1, p2])
        vel.append([v1, v2])
    return np.array(pos), np.array(vel)


def task1():
    pos, vel = load("i.txt")
    plt.ion()
    fig, ax = plt.subplots()
    for t in range(10159, 100000, 1):
        vals = pos + t * vel
        ax.clear()
        ax.plot(vals[:,0], -vals[:, 1], ".")
        ax.axis("equal")
        plt.draw()
        fig.canvas.flush_events()
        time.sleep(100)
        print(t)
