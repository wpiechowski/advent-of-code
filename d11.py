import numpy as np


def load_map(fn: str) -> np.array:
    lines = []
    for line in open(fn):
        l = []
        for ch in line.strip():
            l.append(1 * (ch == "#"))
        lines.append(l)
    lines = np.array(lines)
    return lines


def expand_1d(lines: np.array):
    rows = []
    for r in lines:
        if np.all(r == 0):
            rows.append(r)
        rows.append(r)
    return np.array(rows)


def find_stars(lines: np.array) -> list[tuple[int, int]]:
    ret = []
    for y, row in enumerate(lines):
        for x, val in enumerate(row):
            if val:
                ret.append((x, y))
    return ret


def calc_dists(stars) -> int:
    ret = 0
    for x1, y1 in stars:
        for x2, y2 in stars:
            if x1 == x2 and y1 == y2:
                break
            ret += abs(x1 - x2) + abs(y1 - y2)
    return ret


def task1():
    lines = load_map("i11a.txt")
    lines = expand_1d(lines)
    lines = expand_1d(lines.T).T
    stars = find_stars(lines)
    print(stars)
    print(calc_dists(stars))
