import time
from collections import deque

from tools import get_re_lines
import numpy as np


def load():
    # x y size used avail use%
    fn = "i.txt"
    re_line = r"/dev/grid/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T\s+(\d+)%"
    lines = [tuple(map(int, x)) for x in get_re_lines(fn, re_line)]
    return lines


def is_viable(a: tuple[int, ...], b: tuple[int, ...]) -> bool:
    if a[3] == 0:
        return False
    return a[3] <= b[4]


def task1():
    data = load()
    goods = 0
    for a in data:
        if a[3] == 0:
            ic(a)
        for b in data:
            if a is b:
                continue
            if is_viable(a, b):
                # ic(a, b)
                goods += 1
    ic(goods)


def task2():
    dirs = (
        (0, 1, "R"),
        (0, -1, "L"),
        (1, 0, "D"),
        (-1, 0, "U"),
    )
    data = load()
    size_x = 0
    size_y = 0
    for x, y, *tail in data:
        size_x = max(size_x, x + 1)
        size_y = max(size_y, y + 1)
    blocked = np.zeros((size_y, size_x), bool)
    empty = (0, 0)
    payload = (0, size_x - 1)
    target = 0, 0
    visited = set()
    for x, y, s, u, _, _ in data:
        # used[y + size_y * x] = u
        blocked[y, x] = s > 100
        if u == 0:
            empty = y, x
    # state: tuple(empty), tuple(payload), moves
    state = empty, payload, ""
    q = deque([state])
    pt = time.time()
    while q:
        empty, payload, moves = q.popleft()
        now = time.time()
        if now - pt > 1:
            pt = now
            ic(len(q), len(moves))
        key = empty, payload
        if key in visited:
            continue
        visited.add(key)
        if payload == target:
            ic(len(moves), moves)
            return
        for dy, dx, dn in dirs:
            py, px = empty[0] + dy, empty[1] + dx
            if px < 0 or px >= size_x:
                continue
            if py < 0 or py >= size_y:
                continue
            if blocked[py, px]:
                continue
            if (py, px) == payload:
                payload2 = empty
            else:
                payload2 = payload
            empty2 = py, px
            q.append((empty2, payload2, moves + dn))
