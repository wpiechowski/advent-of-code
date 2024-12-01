from collections import Counter

from tools import *


def load():
    fn = "i.txt"
    rx = r"(\w+) \((\d+)\) -> (.*)"
    data = {}
    for name, _, tail in get_re_lines(fn, rx):
        over = tail.split(", ")
        for o in over:
            data[o] = name
        if name not in data:
            data[name] = ""
    return data


def task1():
    data = load()
    for k, v in data.items():
        if not v:
            ic(k)


def load2():
    fn = "i.txt"
    rx = r"(\w+) \((\d+)\)( -> (.*))?"
    data = {}
    for name, weight, _, tail in get_re_lines(fn, rx):
        weight = int(weight)
        if tail:
            over = tail.split(", ")
            for o in over:
                if o not in data:
                    data[o] = ["", 0, 0]
                data[o][0] = name
        if name not in data:
            data[name] = ["", 0, 0]
        data[name][1] = weight
    return data


def ups(data, node):
    for k, v in data.items():
        if v[0] == node:
            yield k


def subsum(data, node) -> int:
    s = data[node][1]
    for k in ups(data, node):
        s += subsum(data,k)
    return s


def find_imbalance(data, root):
    u = [(subsum(data, n), n) for n in ups(data, root)]
    c = Counter([x[0] for x in u])
    if len(c) == 1:
        return
    cm = c.most_common()[0][0]
    c = c.most_common()[1]
    for cnt, node in u:
        if cnt == c[0]:
            ic(cm, cnt, node, data[node])
            find_imbalance(data, node)


def task2():
    data = load2()
    # ic(data)
    for k, v in data.items():
        if not v[0]:
            root = k
            break
    find_imbalance(data, root)
