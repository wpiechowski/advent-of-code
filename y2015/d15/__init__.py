from tools import get_re_lines
import numpy as np


fn = "i.txt"
re_line = r"\w+: capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)"


def calc_score(lines, amts):
    sums = np.zeros(lines.shape[1], int)
    for ingr in range(len(sums)):
        for amt, line in zip(amts, lines):
            sums[ingr] += amt * line[ingr]
    sums[sums < 0] = 0
    return np.prod(sums[:-1]), sums[-1]


def calc_best(lines):
    amts = np.zeros((len(lines), ), int)
    total = 100
    best = 0
    pos = 0
    while pos < len(amts) - 1:
        pos = 0
        while pos < len(lines) - 1:
            amts[pos] += 1
            if sum(amts[:-1]) > total:
                amts[:pos + 1] = 0
                pos += 1
            else:
                break
        amts[-1] = total - np.sum(amts[:-1])
        s, cal = calc_score(lines, amts)
        if cal != 500:  # task2
            continue
        # print(amts, s)
        best = max(s, best)
    return best


def task1():
    lines = [list(map(int, line)) for line in get_re_lines(fn, re_line)]
    lines = np.array(lines)
    print(lines)
    s = calc_best(lines)
    print(s)
