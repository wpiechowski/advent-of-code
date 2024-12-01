from tools import *


def pos_in_spiral(p: int) -> tuple[int, int]:
    y, x = 0, 0
    ring = 0, 1, 2
    while p >= ring[2]:
        ring = ring[0] + 1, ring[2], (ring[2] + (ring[0] + 1) * 2 * 4)
        x, y = ring[0], -ring[0] + 1
        # ic(ring)
    side = ring[0] * 2
    d = p - ring[1]
    if d < side:
        y = y + d
    elif d < side * 2:
        x = ring[0] - (d - side) - 1
        y = ring[0]
    elif d < side * 3:
        x = -x
        y = ring[0] - (d - side * 2) - 1
    else:
        y -= 1
        x = -ring[0] + (d - side * 3) + 1
    return y, x


def task1():
    n = 265149
    # for n in range(10, 100):
    p = pos_in_spiral(n)
    ic(n, p, abs(p[0]) + abs(p[1]))


def task2():
    vals = {(0, 0): 1}
    limit = 265149
    for n in range(2, 1000000):
        y, x = pos_in_spiral(n)
        s = 0
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                p = y + dy, x + dx
                if p in vals:
                    s += vals[p]
        vals[(y, x)] = s
        ic(n, y, x, s)
        if s > limit:
            break
