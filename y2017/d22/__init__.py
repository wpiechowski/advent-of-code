from tools import *
import numpy as np


def load():
    fn = "i.txt"
    margin = 256
    lines = []
    for line in get_lines(fn):
        lines.append([1 if ch == "#" else 0 for ch in line])
    ss = len(lines)
    sl = ss + 2 * margin
    ret = np.zeros((sl, sl), int)
    ret[margin: margin + ss, margin: margin + ss] = lines
    p0 = margin + (ss - 1) // 2
    return ret, (p0, p0)


def step(area: np.array, pos: tuple[int, int], dir: tuple[int, int]):
    dir = -dir[1], dir[0]
    if area[pos]:
        dir = -dir[0], -dir[1]
    area[pos] = 1 - area[pos]
    pos = pos[0] + dir[0], pos[1] + dir[1]
    return pos, dir


def task1():
    area, pos = load()
    score = 0
    dir = (-1, 0)
    for i in range(10000):
        if area[pos] == 0:
            score += 1
        # ic(pos, dir, area[pos])
        pos, dir = step(area, pos, dir)
        if pos[0] < 0 or pos[1] < 0 or pos[0] >= area.shape[0] or pos[1] >= area.shape[1]:
            raise ValueError(f"{i}: area too small")
    # ic(area)
    ic(score)


def step2(area: np.array, pos: tuple[int, int], dir: tuple[int, int]):
    if area[pos] == 0:
        dir = -dir[1], dir[0]
    elif area[pos] == 1:
        pass
    elif area[pos] == 2:
        dir = dir[1], -dir[0]
    else:
        dir = -dir[0], -dir[1]
    area[pos] = (area[pos] + 1) % 4
    pos = pos[0] + dir[0], pos[1] + dir[1]
    return pos, dir


def paint(area: np.array, pos: tuple[int, int]):
    vals = {
        0: ".",
        1: "W",
        2: "#",
        3: "F",
    }
    for y, line in enumerate(area):
        text = ""
        for x, val in enumerate(line):
            ch = vals[val]
            if (y, x) == pos:
                text += f"[{ch}]"
            else:
                text += f" {ch} "
        ic(text)


def task2():
    area, pos = load()
    area *= 2
    score = 0
    dir = (-1, 0)
    for i in range(10000000):
        if area[pos] == 1:
            score += 1
        # paint(area, pos)
        # ic(pos, dir, area[pos])
        pos, dir = step2(area, pos, dir)
        if pos[0] < 0 or pos[1] < 0 or pos[0] >= area.shape[0] or pos[1] >= area.shape[1]:
            raise ValueError(f"{i}: area too small")
    # ic(area)
    ic(score)
