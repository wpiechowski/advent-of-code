from tools import *


def load_iter(fn: str):
    for line in get_lines(fn):
        a, b = line.split(")")
        yield a, b


def task1():
    fn = "i.txt"
    data = {b: a for a, b in load_iter(fn)}
    ret = 0
    for v in data.keys():
        while v in data:
            ret += 1
            v = data[v]
    print(ret)


def path(data: dict[str, str], obj: str) -> list[str]:
    ret = []
    while obj in data:
        obj = data[obj]
        ret.append(obj)
    return ret


def task2():
    fn = "i.txt"
    data = {b: a for a, b in load_iter(fn)}
    p1 = path(data, "YOU")
    p2 = path(data, "SAN")
    print(p1)
    print(p2)
    k = -1
    while True:
        if p1[k] != p2[k]:
            break
        k -= 1
    k += 1
    print(k, len(p1) + len(p2) + 2 * k)
