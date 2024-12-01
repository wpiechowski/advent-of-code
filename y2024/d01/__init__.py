from tools import *


def task1():
    fn = "input"
    l1 = []
    l2 = []
    for a, b in get_int_lines(fn):
        l1.append(a)
        l2.append(b)
    l1.sort()
    l2.sort()
    d = 0
    for a, b in zip(l1, l2):
        d += abs(a-b)
    print(d)


def task2():
    fn = "input"
    l1 = []
    l2 = []
    for a, b in get_int_lines(fn):
        l1.append(a)
        l2.append(b)
    c2 = Counter(l2)
    d = 0
    for a in l1:
        c = c2[a]
        d += a * c
    print(d)
