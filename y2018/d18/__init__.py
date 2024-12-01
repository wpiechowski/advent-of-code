import matplotlib.pyplot as plt

from tools import *
import numpy as np


MAP_G = 0
MAP_T = 1
MAP_L = 2


def load(fn: str) -> np.array:
    data = []
    vals = {
        ".": MAP_G,
        "|": MAP_T,
        "#": MAP_L,
    }
    for line in get_lines(fn):
        data.append([])
        for ch in line:
            data[-1].append(vals[ch])
    return np.array(data)


def step(data: np.array) -> np.array:
    ret = np.zeros(data.shape, int)
    for y in range(data.shape[0]):
        sub_y = slice(max(0, y - 1), min(data.shape[0], y + 2))
        for x in range(data.shape[1]):
            sub_x = slice(max(0, x - 1), min(data.shape[1], x + 2))
            area = data[sub_y, sub_x]
            if data[y, x] == MAP_G:
                if np.sum(area == MAP_T) >= 3:
                    ret[y, x] = MAP_T
                else:
                    ret[y, x] = MAP_G
            elif data[y, x] == MAP_T:
                if np.sum(area == MAP_L) >= 3:
                    ret[y, x] = MAP_L
                else:
                    ret[y, x] = MAP_T
            elif data[y, x] == MAP_L:
                if np.sum(area == MAP_L) >= 2 and np.sum(area == MAP_T) >= 1:
                    ret[y, x] = MAP_L
                else:
                    ret[y, x] = MAP_G
    return ret


def task1():
    data = load("i.txt")
    plt.ion()
    fig, ax = plt.subplots()
    img = ax.imshow(data)
    d_ref = None
    for n in range(1000000000):
        # ic(n, data)
        n += 1
        ic(n)
        data = step(data)
        score = np.sum(data == MAP_T) * np.sum(data == MAP_L)
        ic(n, score)
        img.set_data(data)
        ax.set_title(f"{n}")
        plt.draw()
        fig.canvas.flush_events()
        if n == 500:
            d_ref = np.copy(data)
        elif n > 500:
            if np.all(d_ref == data):
                break
    p = (1000000000 - 500) % (n - 500)
    ic(p + 500)
