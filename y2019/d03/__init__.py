from itertools import pairwise

from tools import *


def load(fn: str):
    return [line.split(",") for line in get_lines(fn)]


def trace(path: list[str]):
    pts = [(0, 0)]
    dirs = {ch: (dy, dx) for dy, dx, ch, _ in directions}
    for p in path:
        d = p[0]
        l = int(p[1:])
        py = pts[-1][0] + dirs[d][0] * l
        px = pts[-1][1] + dirs[d][1] * l
        pts.append((py, px))
    return pts


def collide(a1, a2, b1, b2):
    for d in (0, 1):
        if max(a1[d], a2[d]) <= min(b1[d], b2[d]):
            return
        if min(a1[d], a2[d]) >= max(b1[d], b2[d]):
            return
    if a1[0] == a2[0]:
        if b1[0] == b2[0]:
            raise "parallel"
        yield a1[0], b1[1]
    else:
        yield b1[0], a1[1]


def iter_collisions(paths):
    for a1, a2 in pairwise(paths[0]):
        print(a1)
        for b1, b2 in pairwise(paths[1]):
            for c in collide(a1, a2, b1, b2):
                d = abs(c[0]) + abs(c[1])
                yield d


def task1():
    paths = list(map(trace, load("i.txt")))
    print(min(iter_collisions(paths)))


def iter_collisions2(paths):
    dist1 = 0
    for a1, a2 in pairwise(paths[0]):
        print(a1)
        dist2 = 0
        for b1, b2 in pairwise(paths[1]):
            for c in collide(a1, a2, b1, b2):
                d = dist1 + abs(c[0] - a1[0]) + abs(c[1] - a1[1]) + dist2 + abs(c[0] - b1[0]) + abs(c[1] - b1[1])
                yield d
            dist2 += abs(b2[0] - b1[0]) + abs(b2[1] - b1[1])
        dist1 += abs(a2[0] - a1[0]) + abs(a2[1] - a1[1])


def task2():
    paths = list(map(trace, load("i.txt")))
    print(min(iter_collisions2(paths)))
