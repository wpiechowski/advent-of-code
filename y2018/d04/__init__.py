from tools import *
import numpy as np


def load(fn: str):
    rx = r"\[(\d+)-(\d+)-(\d+) (\d+):(\d+)\] (Guard #(\d+) )?(.+)"
    for match in get_re_lines(fn, rx):
        year, mon, day, h, m, _, g, c = match
        year = int(year)
        mon = int(mon)
        day = int(day)
        h = int(h)
        m = int(m)
        if g:
            g = int(g)
            if not g:
                raise ValueError("guard 0")
        else:
            g = 0
        code = 0
        if c[0] == "b":
            code = 0
        elif c[0] == "f":
            code = 1
        elif c[0] == "w":
            code = -1
        yield [year, mon, day, h, m, g, code]


def insert_guards(vals: list) -> set[int]:
    ret = set()
    last = None
    for val in vals:
        g = val[5]
        if g:
            last = g
            ret.add(g)
        else:
            val[5] = last
    return ret


def check_guard(vals: list, guard: int) -> tuple[int, int, int]:
    data = np.zeros((60,), int)
    sleep_start = 100
    for _, _, _, _, m, g, code in vals:
        if g != guard:
            continue
        if code == 1:
            sleep_start = m
        elif code == -1:
            data[sleep_start: m] += 1
    n = np.argmax(data)
    return n, data[n], sum(data)


def task1():
    vals = list(load("i.txt"))
    vals.sort()
    guards = insert_guards(vals)
    # ic(vals)
    # ic(len(vals))
    # ic(guards)
    best_guard = 0
    best_minute = 0
    best_count = 0
    best_total = 0
    for guard in guards:
        m, c, t = check_guard(vals, guard)
        ic(guard, m, c, t)
        # if t > best_total:  # task1
        if c > best_count:  # task2
            best_guard = guard
            best_minute = m
            best_count = c
            best_total = t
    ic(best_guard, best_minute, best_count, best_guard * best_minute)
