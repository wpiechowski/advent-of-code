from itertools import pairwise

from tools import *


def is_good(p: int) -> bool:
    vals = [int(x) for x in str(p)]
    d = 0
    for a, b in pairwise(vals):
        if a == b:
            d = True
        if a > b:
            return False
    return d


def task1():
    r = range(136760, 595730+1)
    goods = 0
    for p in r:
        if is_good(p):
            goods += 1
    print(goods)


def is_good2(p: int) -> bool:
    vals = [int(x) for x in str(p)] + [10]
    a = -1
    in_pair = False
    invalid = False
    good = False
    for b, c in pairwise(vals):
        if b > c:
            return False
        if b != c and in_pair and not invalid:
            good = True
        in_pair = b == c
        invalid = a == b and b == c
        a = b
    return good


def task2():
    r = range(136760, 595730+1)
    goods = 0
    for p in r:
        if is_good2(p):
            goods += 1
    print(goods)
