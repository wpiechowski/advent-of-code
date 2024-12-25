from tools import *
import numpy as np


def process(lines: list[str]) -> np.array:
    vals = np.zeros((5,), dtype=int)
    if lines[0][0] == ".":
        lines = reversed(lines)
    for y, line in enumerate(lines):
        for x, ch in enumerate(line):
            if ch == "#":
                vals[x] = y
    return vals


def load(fn: str) -> tuple[list[np.array], list[np.array]]:
    items = [[], []]    # keys, locks
    cur = []
    for line in get_lines(fn):
        if line:
            cur.append(line)
        else:
            if cur:
                index = int(cur[0][0] == "#")
                items[index].append(process(cur))
            cur = []
    if cur:
        index = int(cur[0][0] == "#")
        items[index].append(process(cur))
    return items[0], items[1]


def task1():
    keys, locks = load("i.txt")
    score = 0
    for k in keys:
        for l in locks:
            if np.all(k + l <= 5):
                # print(k, l)
                score += 1
    print(score)
