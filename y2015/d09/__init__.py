import numpy as np
import re
from itertools import permutations


def load_graph(fn: str) -> np.array:
    names = {}
    next_id = 0
    dist = {}
    re_line = re.compile(r"(.+) to (.+) = (\d+)")
    for line in open(fn):
        m = re_line.match(line.strip())
        for n in (m[1], m[2]):
            if n not in names:
                names[n] = next_id
                next_id += 1
        dist[(names[m[1]], names[m[2]])] = int(m[3])
    ret = np.zeros((next_id, next_id), int)
    for (i1, i2), d in dist.items():
        ret[i1, i2] = d
        ret[i2, i1] = d
    return ret


def find_shortest(dist: np.array) -> int:
    best = 0
    for p in permutations(range(len(dist))):
        d = 0
        h = p[0]
        for z in p[1:]:
            d += dist[h, z]
            h = z
        best = max(d, best)
    return best


def task1():
    fn = "y2015/d09/i.txt"
    dist = load_graph(fn)
    print(dist)
    d = find_shortest(dist)
    print(d)
