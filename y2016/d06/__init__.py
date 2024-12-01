import collections

from tools import get_lines

fn = "i.txt"


def count(fn: str):
    counters = []
    for line in get_lines(fn):
        if not counters:
            for _ in line:
                counters.append(collections.Counter())
        for c, ch in zip(counters, line):
            c.update(ch)
    return counters


def task1():
    ret = ""
    counters = count(fn)
    for c in counters:
        m = c.most_common(1)[0]
        print(m)
        ret += m[0]
    print(ret)


def task2():
    ret = ""
    counters = count(fn)
    for c in counters:
        m = c.most_common()[-1]
        print(m)
        ret += m[0]
    print(ret)
