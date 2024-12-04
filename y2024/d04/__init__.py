import re

from tools import *


rx = re.compile(r"XMAS")


def calc_xmax(lines):
    ret = 0
    for line in lines:
        for m in rx.finditer(line):
            ret += 1
    return ret


def rot(lines):
    ret = ["" for _ in lines[0]]
    for line in lines:
        for x, ch in enumerate(line):
            ret[len(lines[0]) - 1 - x] += ch
    return ret


def diag(lines):
    ret = []
    for y in range(2 * len(lines)):
        line = ""
        for x in range(len(lines[0])):
            yy = y - x
            if 0 <= yy < len(lines):
                ch = lines[yy][x]
                line += ch
        ret.append(line)
    return ret


def pr(lines):
    for line in lines:
        print(line)


def task1():
    fn = "i.txt"
    lines = list(get_lines(fn))
    count = 0
    for r in range(4):
        # print("--------------", r)
        # pr(lines)
        count += calc_xmax(lines)
        d = diag(lines)
        count += calc_xmax(d)
        lines = rot(lines)
    print(count)


def task2():
    fn = "i.txt"
    lines = list(get_lines(fn))
    cnt = 0
    for y in range(1, len(lines) - 1):
        for x in range(1, len(lines[0]) - 1):
            if lines[y][x] != "A":
                continue
            d1 = lines[y-1][x-1] + lines[y+1][x+1]
            d2 = lines[y-1][x+1] + lines[y+1][x-1]
            if d1 in ("MS", "SM") and d2 in ("MS", "SM"):
                cnt += 1
    print(cnt)
