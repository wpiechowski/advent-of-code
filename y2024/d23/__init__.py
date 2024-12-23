from tools import *


def load(fn: str) -> tuple[set[str], set[tuple[str]]]:
    ret = set()
    nodes = set()
    for line in get_lines(fn):
        a, b = sorted(line.split("-"))
        ret.add((a, b))
        # ret.add((b, a))
        nodes.add(a)
        nodes.add(b)
    return nodes, ret


def task1():
    _, edges = load("i.txt")
    print(edges)
    tris = set()
    for a, b in edges:
        for c, d in edges:
            if (a, b) == (c, d):
                continue
            if c in (a, b):
                t = d
            else:
                t = c
            if not (a.startswith("t") or b.startswith("t") or c.startswith("t")):
                continue
            if ((a, t) in edges or (t, a) in edges) and ((b, t) in edges or (t, b) in edges):
                tris.add(tuple(sorted([a, b, t])))
    print(len(tris))


def one_more(nodes: set[str], edges: set[tuple[str]], cliques: set[tuple[str]]) -> set[tuple[str]]:
    ret = set()
    for n, cur in enumerate(cliques):
        print(f"len={len(cur)} {n}/{len(cliques)} cur len {len(ret)}")
        for nut in nodes:
            for node in cur:
                if (node, nut) not in edges and (nut, node) not in edges:
                    break
            else:
                ret.add(tuple(sorted(list(cur) + [nut])))
    return ret


def task2():
    nodes, edges = load("i.txt")
    cliques = edges
    count = 2
    while True:
        print(count, len(cliques))
        step = one_more(nodes, edges, cliques)
        if not step:
            break
        cliques = step
        count += 1
    print(cliques)
    for c in cliques:
        print(",".join(c))
