from tools import *
import numpy as np


def load(fn: str):
    zeros = []
    data = []
    for y, line in enumerate(get_lines(fn)):
        cur = []
        for x, ch in enumerate(line):
            if ch == ".":
                ch = 20
            else:
                ch = int(ch)
            if ch == 0:
                zeros.append((y, x))
            cur.append(ch)
        data.append(cur)
    return np.array(data, dtype=int), zeros


def calc_score(arr: np.array, scores: dict[tuple[int, int], set], pt: tuple[int, int]) -> set:
    if pt in scores:
        return scores[pt]
    h = arr[pt]
    if h == 9:
        scores[pt] = {pt}
        return scores[pt]
    scores[pt] = set()
    for dy, dx, _, _ in directions:
        y = pt[0] + dy
        x = pt[1] + dx
        if not 0 <= y < arr.shape[0]:
            continue
        if not 0 <= x < arr.shape[1]:
            continue
        if arr[y, x] != h + 1:
            continue
        scores[pt] |= calc_score(arr, scores, (y, x))
    return scores[pt]


def task1():
    arr, zeros = load("i.txt")
    scores = {}
    ret = 0
    for pt in zeros:
        ret += len(calc_score(arr, scores, pt))
    print(ret)


def calc_score2(arr: np.array, scores: np.array, pt: tuple[int, int]) -> int:
    if scores[pt] >= 0:
        return scores[pt]
    h = arr[pt]
    if h == 9:
        scores[pt] = 1
        return scores[pt]
    scores[pt] = 0
    for dy, dx, _, _ in directions:
        y = pt[0] + dy
        x = pt[1] + dx
        if not 0 <= y < arr.shape[0]:
            continue
        if not 0 <= x < arr.shape[1]:
            continue
        if arr[y, x] != h + 1:
            continue
        scores[pt] += calc_score2(arr, scores, (y, x))
    return scores[pt]


def task2():
    arr, zeros = load("i.txt")
    scores = -np.ones(arr.shape, dtype=int)
    ret = 0
    for pt in zeros:
        ret += calc_score2(arr, scores, pt)
    print(ret)
