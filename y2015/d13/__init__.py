import numpy as np
import re
from itertools import permutations


def load_graph(fn: str) -> np.array:
    names: dict[str, int] = {}
    next_id = 0
    data: dict[tuple[int, int], int] = {}
    re_line = re.compile(r"(\w+) would (gain|lose) (\d+) happiness units by sitting next to (\w+).+")
    for line in open(fn):
        m = re_line.match(line)
        n1, gl, val, n2 = m[1], m[2], m[3], m[4]
        for n in (n1, n2):
            if n not in names:
                names[n] = next_id
                next_id += 1
        i1 = names[n1]
        i2 = names[n2]
        data[i1, i2] = int(val) * (1 if gl == "gain" else -1)
    a = np.zeros((next_id, next_id), int)
    for k, v in data.items():
        a[k] = v
    return a


def find_seats(g: np.array):
    best = 0
    for pos in permutations(range(1, len(g))):
        pos = pos + (0,)
        h = 0
        score = 0
        for p in pos:
            score += g[h, p] + g[p, h]
            h = p
        print(pos, score)
        best = max(best, score)
    print(best)


fn = "y2015/d13/i.txt"


def task1():
    g = load_graph(fn)
    find_seats(g)


def task2():
    g = load_graph(fn)
    a = np.zeros((len(g) + 1, len(g) + 1), int)
    a[1:, 1:] = g
    find_seats(a)
