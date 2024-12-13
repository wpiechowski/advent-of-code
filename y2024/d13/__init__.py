from tools import *


def load_iter(fn: str):
    lines = []
    for line in get_lines(fn):
        i = row_of_ints(line)
        if not i:
            continue
        lines.append(i)
        if line.startswith("P"):
            yield lines
            lines = []


def calc_item(item: list[list[int]]):
    ((ax, ay), (bx, by), (px, py)) = item
    for n in range(px // bx, 0, -1):
        kx = n * bx
        t = px - kx
        q, r = divmod(t, ax)
        if not r:
            if n * by + q * ay == py:
                return q, n
    return 0, 0


def task1():
    score = 0
    for item in load_iter("i.txt"):
        print(item)
        a, b = calc_item(item)
        print(a, b)
        score += a * 3 + b
    print(score)


def calc_item2(item: list[list[int]]):
    ((ax, ay), (bx, by), (px, py)) = item
    if ax * by == ay * bx:
        print(item)
        raise ValueError("parallel")
    print(item)
    # y = (ay/ax)x
    # ax*y = ay*x

    # bx*y = by*x + c
    # bx*py = by*px + c

    c = bx*py - by*px

    # bx*(ay/ax)*x = by*x + c
    # bx*ay*x = by*ax*x + c*ax
    # x(bx*ay - by*ax) = c*ax
    xq, xr = divmod(c * ax, bx * ay - by * ax)
    if xr:
        return 0, 0
    pa, ra = divmod(xq, ax)
    pb, rb = divmod(px - xq, bx)
    print(xq, xr)
    print(pa, pb, ra, rb)
    if ra or rb:
        return 0, 0
    return pa, pb


def task2():
    score = 0
    for item in load_iter("i.txt"):
        item[2] = [i + 10000000000000 for i in item[2]]
        a, b = calc_item2(item)
        score += a * 3 + b
    print(score)
