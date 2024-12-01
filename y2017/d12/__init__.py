from tools import *


def load(fn):
    rx = r"(\d+) <-> (.+)"
    g = {}
    for n1, nn in get_re_lines(fn, rx):
        n1 = int(n1)
        nn = row_of_ints(nn)
        g[n1] = set(nn)
    return g


def count_group(g: dict[int, set[int]], n0: int) -> set[int]:
    q = [n0]
    grp = set()
    while q:
        n = q.pop()
        if n in grp:
            continue
        grp.add(n)
        q.extend(g[n])
    return grp


def count_groups(g: dict[int, set[int]]) -> int:
    unknowns = set(g.keys())
    grp_count = 0
    while unknowns:
        n = unknowns.pop()
        grp = count_group(g, n)
        unknowns -= grp
        grp_count += 1
    return grp_count


def task1():
    g = load("i.txt")
    grp = count_group(g, 0)
    ic(len(grp))


def task2():
    g = load("i.txt")
    c = count_groups(g)
    ic(c)
