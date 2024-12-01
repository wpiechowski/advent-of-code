from tools import *


def gen(s: int, mul: int, mask: int):
    while True:
        s = (s * mul) % 2147483647
        if s & mask == 0:
            yield s


def task1():
    g1 = gen(873, 16807, 3)
    g2 = gen(583, 48271, 7)
    ret = 0
    for n, c1, c2 in zip(range(5000000), g1, g2):
        if (c1 ^ c2) & 0xffff == 0:
            ret += 1
            ic(n, c1, c2)
    ic(ret)
