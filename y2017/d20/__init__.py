from tools import *
import math


def task1():
    best_n = 0
    best_acc = None
    for n, vals in enumerate(get_int_lines("i.txt")):
        acc = abs(vals[-1]) + abs(vals[-2]) + abs(vals[-3])
        if best_acc is None or best_acc > acc:
            best_n = n
            best_acc = acc
    ic(best_n)


def solve(aa: int, b: int, c: int):
    a = aa / 2
    b += a
    if aa == 0:
        # bx+c=0
        if b:
            t = -c / b
            if t >= 0 and t == int(t):
                return [t]
            return []
        if c:
            return []
        # ic("equal")
        return [-1]
    d = b**2 - 4*a*c
    if d < 0:
        return []
    ds = math.sqrt(d)
    # if int(ds) != ds:
    #     return []
    # ds = int(ds)
    t1 = (-b - ds) / aa
    t2 = (-b + ds) / aa
    ret = []
    for t in (t1, t2):
        if t >= 0 and abs(t - round(t)) < 1e-5:
            ret.append(int(round(t)))
    return ret


def calc_pos(d: list[int], t: int) -> tuple[int, ...]:
    ret = []
    for dim in range(3):
        p, v, a = d[dim::3]
        s = int(p + t * v + t * (t + 1) * a / 2)
        ret.append(s)
    return tuple(ret)


def collide(d1: list, d2: list):
    times = []
    for dim in range(3):
        tt = solve(d1[dim + 6] - d2[dim + 6],
                   d1[dim + 3] - d2[dim + 3],
                   d1[dim] - d2[dim])
        # if tt:
        #     ic(d1[:3], d2[:3], tt)
        if tt and tt[0] < 0:
            continue
        times.append(set(tt))
    if not times:
        raise "infinity"
    result = times[0]
    for t in times[1:]:
        result &= t
    ret = []
    if result:
        # ic(d1, d2, times)
        for t in list(result):
            ret.append((t, calc_pos(d1, t)))
    return ret


def sim(p1: list[int], p2: list[int]):
    p1 = p1.copy()
    p2 = p2.copy()
    steps = 40
    for t in range(steps):
        ic(t, p1[:3], p2[:3])
        for p in (p1, p2):
            for d in range(3):
                p[d + 3] += p[d + 6]
                p[d] += p[d + 3]


def task2():
    data = list(get_int_lines("i.txt"))
    # n1, n2 = 338, 334
    # collide(data[n1], data[n2])
    # sim(data[n1], data[n2])
    # return
    colls = []
    for n1, d1 in enumerate(data):
        for n2, d2 in enumerate(data[:n1]):
            for t, pos in collide(d1, d2):
                colls.append((t, pos, n1, n2))
    colls.sort()
    ic(colls)
    killed = {}
    for t, pos, n1, n2 in colls:
        for n in (n1, n2):
            if n in killed and killed[n] < t:
                break
        else:
            killed[n1] = t
            killed[n2] = t
    ic(len(data) - len(killed))
