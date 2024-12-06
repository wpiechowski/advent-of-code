from tools import *
import numpy as np


def load(fn: str) -> tuple[np.array, tuple, int]:
    data = []
    pos = None
    head_n = -1
    for y, line in enumerate(get_lines(fn)):
        vals = []
        for x, ch in enumerate(line):
            vals.append(ch=="#")
            if ch in "<>v^":
                pos = y, x
                for n, (_, _, _, code) in enumerate(directions):
                    if code == ch:
                        head_n = n
        data.append(vals)
    ret = np.array(data, dtype=int)
    return ret, pos, head_n


def task1():
    arr, (py, px), head_n = load("i.txt")
    while True:
        arr[py, px] = 2
        dy, dx, _, _ = directions[head_n]
        p2y, p2x = py + dy, px + dx
        if not (0 <= p2y < arr.shape[0] and 0 <= p2x < arr.shape[1]):
            break
        if arr[p2y, p2x] == 1:
            head_n = (head_n + 1) % 4
        else:
            py, px = p2y, p2x
    # print(arr)
    print(np.sum(arr==2))


def check_for_loop(arr: np.array, p: tuple[int, int], head_n: int) -> bool:
    py, px = p
    while True:
        dy, dx, _, _ = directions[head_n]
        p2y, p2x = py + dy, px + dx
        if not (0 <= p2y < arr.shape[0] and 0 <= p2x < arr.shape[1]):
            return False
        if arr[p2y, p2x] == -1:
            head_n = (head_n + 1) % 4
        else:
            py, px = p2y, p2x
        if arr[py, px] & (1 << head_n):
            return True
        arr[py, px] |= 1 << head_n


def task2():
    arr, (py, px), head_n = load("i.txt")
    arr = -arr
    arr[py, px] = 1 << head_n
    loops = 0
    for iy, ix in np.ndindex(arr.shape):
        print(iy, ix)
        if arr[iy, ix] != 0:
            continue
        a = arr.copy()
        a[iy, ix] = -1
        if check_for_loop(a, (py, px), head_n):
            loops += 1
    print(loops)
