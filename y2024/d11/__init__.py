from itertools import chain

from tools import *


def task1():
    fn = "i1.txt"
    iters = 25
    stones = []
    for line in get_int_lines(fn):
        stones.extend(line)
    for i in range(iters):
        adds = []
        for n, s in enumerate(stones):
            k = str(s)
            if s == 0:
                stones[n] = 1
            elif len(k) & 1 == 0:
                s1 = int(k[:len(k)//2])
                s2 = int(k[len(k)//2:])
                stones[n] = s1
                adds.append(s2)
            else:
                stones[n] *= 2024
        stones.extend(adds)
        print(i, len(stones))


def process_stone(s):
    k = str(s)
    if s == 0:
        return 1,
    elif len(k) & 1 == 0:
        s1 = int(k[:len(k) // 2])
        s2 = int(k[len(k) // 2:])
        return s1, s2
    else:
        return s * 2024,


@cache
def iterate_stone(stone: int, iters: int) -> int:
    if iters == 0:
        return 1
    news = process_stone(stone)
    ret = 0
    for n in news:
        ret += iterate_stone(n, iters - 1)
    return ret


def task2():
    fn = "i.txt"
    iters = 75
    stones = []
    for line in get_int_lines(fn):
        stones.extend(line)
    score = 0
    for stone in stones:
        score += iterate_stone(stone, iters)
    print(score)
