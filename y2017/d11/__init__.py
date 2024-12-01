from collections import Counter

from tools import *


def count_steps(line: str):
    x = 0
    y = 0
    dirs = {
        "n": (0, 2),
        "ne": (1, 1),
        "se": (1, -1),
        "s": (0, -2),
        "sw": (-1, -1),
        "nw": (-1, 1),
    }
    counter = Counter(line.split(","))
    for d, cnt in counter.most_common():
        dx, dy = dirs[d]
        x += dx * cnt
        y += dy * cnt
    x = abs(x)
    y = abs(y)
    if y >= x:
        v = (y - x) // 2
    else:
        v = 0
    steps = v + x
    ic(x, y, steps)


def steps_from_pos(x, y):
    x = abs(x)
    y = abs(y)
    if y >= x:
        v = (y - x) // 2
    else:
        v = 0
    steps = v + x
    return steps


def count_steps2(line: str):
    x = 0
    y = 0
    dirs = {
        "n": (0, 2),
        "ne": (1, 1),
        "se": (1, -1),
        "s": (0, -2),
        "sw": (-1, -1),
        "nw": (-1, 1),
    }
    furthest = 0
    for d in line.split(","):
        dx, dy = dirs[d]
        x += dx
        y += dy
        steps = steps_from_pos(x, y)
        furthest = max(furthest, steps)
    ic(x, y, steps, furthest)


def task1():
    for line in get_lines("i.txt"):
        count_steps2(line)
