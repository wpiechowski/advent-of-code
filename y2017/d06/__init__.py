from tools import *


def step(vals: list[int]):
    n = vals.index(max(vals))
    cnt = vals[n]
    vals[n] = 0
    for _ in range(cnt):
        n = (n + 1) % len(vals)
        vals[n] += 1
    return vals


def test(vals: list[int]):
    seen = {tuple(vals)}
    steps = 0
    while True:
        step(vals)
        steps += 1
        t = tuple(vals)
        if t in seen:
            ic(steps)
            return
        seen.add(t)


def task1():
    for vals in get_int_lines("i.txt"):
        test(vals)


def task2():
    for vals in get_int_lines("i.txt"):
        test(vals)
        test(vals)
