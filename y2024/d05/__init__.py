from tools import *
import numpy as np


def load(fn: str):
    rels = []
    lists = []
    re_rel = re.compile(r"(\d+)\|(\d+)")
    for line in get_lines(fn):
        if "|" in line:
            a, b = list(map(int, line.split("|")))
            rels.append((a, b))
        elif "," in line:
            lists.append(row_of_ints(line))
    arr = np.zeros((100, 100), dtype=int)
    for a, b in rels:
        arr[a, b] = 1
        arr[b, a] = -1
    return arr, lists


def check_line(line, arr) -> int:
    errs = 0
    for i in range(len(line) - 1):
        for j in range(i+1, len(line)):
            if arr[line[i], line[j]] < 0:
                errs += 1
    return errs


def task1():
    fn = "i.txt"
    arr, lists = load(fn)
    ret = 0
    for line in lists:
        if check_line(line, arr) == 0:
            # print(line)
            ret += line[len(line) // 2]
    print(ret)


def is_head(item: int, others: list[int], arr) -> bool:
    for e in others:
        if arr[item, e] < 0:
            return False
    return True


def fix_line(line: list[int], arr):
    ret = []
    while line:
        for item in line:
            if is_head(item, line, arr):
                ret.append(item)
                line.remove(item)
                break
    return ret


def task2():
    fn = "i.txt"
    arr, lists = load(fn)
    ret = 0
    for line in lists:
        c = check_line(line, arr)
        if c == 0:
            continue
        line = fix_line(line, arr)
        # print(line)
        ret += line[len(line) // 2]
    print(ret)
