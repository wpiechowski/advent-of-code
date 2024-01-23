import re
from collections import Counter


re_sth = re.compile(r"\\(\\|\"|x..)")


def calc_delta(s: str) -> int:
    s2 = re_sth.sub("=", s)
    return len(s) - (len(s2) - 2)


def task1():
    fn = "y2015/d08/i.txt"
    total = 0
    for line in open(fn):
        line = line.strip()
        delta = calc_delta(line)
        print(line, delta)
        total += delta
    print(total)


def delta2(s: str) -> int:
    c = Counter(s)
    return c["\\"] + c["\""] + 2


def task2():
    fn = "y2015/d08/i.txt"
    total = 0
    for line in open(fn):
        line = line.strip()
        delta = delta2(line)
        total += delta
        print(line, delta)
    print(total)
