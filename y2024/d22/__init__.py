from collections import defaultdict

import numpy

from tools import *
import numpy as np


def next_secret(val: int) -> int:
    val = ((val << 6) ^ val) & 0xffffff
    val = ((val >> 5) ^ val) & 0xffffff
    val = ((val << 11) ^ val) & 0xffffff
    return val


def task1():
    score = 0
    for val, in get_int_lines("i.txt"):
        v0 = val
        for _ in range(2000):
            val = next_secret(val)
        print(f"{v0}: {val}")
        score += val
    print(score)


def gen_data(val: int, count: int) -> np.array:
    r = np.zeros((count,), dtype=int)
    for n in range(count):
        r[n] = val % 10
        val = next_secret(val)
    return r


def best_dict(scores: dict) -> tuple:
    best_k, best_v = None, 0
    for k, v in scores.items():
        if v > best_v:
            best_k, best_v = k, v
    return best_k, best_v


def task2():
    # k_ref = -2, 1, -1, 3
    vals = [x for x, in get_int_lines("i.txt")]
    scores = defaultdict(int)
    for val in vals:
        print(val)
        v0 = val
        prices = gen_data(val, 2001)
        d = np.diff(prices)
        cur_scores = {}
        for n in range(len(prices) - 4):
            key = tuple(map(int, d[n: n+4]))
            price = int(prices[n + 4])
            if key not in cur_scores:
                cur_scores[key] = price
        # print(v0, best_dict(cur_scores))
        for key, price in cur_scores.items():
            scores[key] += price
    bk, bv = best_dict(scores)
    print(bk, bv)
    test_seq(vals, bk)
    # print(k_ref, scores[k_ref])


def test_seq(vals: list[int], seq: tuple[int]):
    score = 0
    for val in vals:
        # print(val)
        v0 = val
        prices = gen_data(val, 2001)
        d = np.diff(prices)
        for n in range(len(prices) - 4):
            key = tuple(map(int, d[n: n+4]))
            price = int(prices[n + 4])
            if key == seq:
                score += price
                # print(v0, n, price)
                break
    print(score)


numpy.set_printoptions(legacy="1.25")

# 0,0,-1,1 1598 ... 1607
# 1598 -
# 1599
# 1600
# 1601
# 1602
# 1603 -
# 1604
# 1605
# 1606
# 1607 -
