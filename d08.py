from itertools import cycle, chain
import numpy as np
from math import lcm


def task1():
    nodes = {}
    f = open("i08a.txt")
    cmds = next(f).strip()
    next(f)
    for line in f:
        node, left, right = line[:3], line[7:10], line[12:15]
        nodes[node] = (left, right)
    steps = 0
    here = "AAA"
    for cmd in cycle(cmds):
        if cmd == "L":
            here = nodes[here][0]
        else:
            here = nodes[here][1]
        steps += 1
        print(here, steps)
        if here == "ZZZ":
            break


def find_path(nodes: dict, node: str, cmds: str, offset: int, cache: dict):
    i_cmd = chain(cmds[offset:], cycle(cmds))
    path = []
    visited = set()
    # print(f"check path for {node} {offset}")
    while True:
        path.append(node)
        visited.add((node, offset % len(cmds)))
        d = next(i_cmd)
        offset = (offset + 1) % len(cmds)
        if d == "L":
            node = nodes[node][0]
        else:
            node = nodes[node][1]
        # print(f"next node {d} {node} {offset}")
        if node[2] == "Z":
            return path, node, len(path), True
        if (node, offset) in cache:
            c = cache[node, offset]
            return path, c[0], c[1] + len(path), c[1] >= 0
        if (node, offset) in visited:
            return path, node, -1, False


def fill_cache(nodes: dict, cmds: str) -> dict[(str, int), (str, int)]:
    cache = {}  # node, cmd_offset -> cycle count / -1
    for node in nodes.keys():
        for offset in range(len(cmds)):
            if (node, offset) in cache:
                continue
            path, landed, count, success = find_path(nodes, node, cmds, offset, cache)
            for o2, n in enumerate(path):
                cache[n, (offset + o2) % len(cmds)] = (landed, count - o2 if success else -1)
    return cache


def task2_():
    nodes = {}
    f = open("i08a.txt")
    cmds = next(f).strip()
    next(f)
    here = []
    for line in f:
        node, left, right = line[:3], line[7:10], line[12:15]
        nodes[node] = (left, right)
        if node[2] == "A":
            here.append(node)
    # p = find_path(nodes, "RLZ", cmds, 0, {})
    # print(p)
    # return
    cache = fill_cache(nodes, cmds)
    # for k, v in cache.items():
    #     print(k, v)
    steps = np.zeros((len(here), ), dtype=int)
    while True:
        print(here, steps, steps % len(cmds))
        i = np.argmin(steps)
        c = cache[here[i], steps[i] % len(cmds)]
        if c[1] < 0:
            print(f"failed at {here[i]}, {steps[i]}: {c}")
            break
        steps[i] += c[1]
        here[i] = c[0]
        if np.all(steps == steps[0]):
            print("good")
            print(steps)
            break


def task2():
    print(lcm(17873, 12599, 21389, 17287, 13771, 15529))