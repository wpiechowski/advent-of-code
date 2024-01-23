import numpy as np


def load_line(line: str) -> list[int]:
    ret = []
    for ch in line:
        ret.append(1 if ch == "#" else 0)
    return ret


def iter_patterns(fn):
    pat = []
    for line in open(fn):
        line = line.strip()
        if not line:
            yield np.array(pat)
            pat = []
        else:
            pat.append(load_line(line))
    if pat:
        yield np.array(pat)


def check_sym(pat: np.array, y: int) -> bool:
    cnt = min(y, pat.shape[0] - y)
    for n in range(cnt):
        if not np.all(pat[y - n - 1, :] == pat[y + n]):
            return False
    return True


def check_sym2(pat: np.array, y: int) -> bool:
    cnt = min(y, pat.shape[0] - y)
    holes = 0
    for n in range(cnt):
        h = np.sum(pat[y - n - 1, :] != pat[y + n])
        holes += h
    return holes == 1


def process_pattern(pat: np.array, fun) -> int:
    for y in range(1, pat.shape[0]):
        if fun(pat, y):
            return y * 100
    p2 = pat.T
    for x in range(1, p2.shape[0]):
        if fun(p2, x):
            return x


def task(fun):
    ret = 0
    for pat in iter_patterns("i13a.txt"):
        s = process_pattern(pat, fun)
        ret += s
        print(s)
    print(ret)


def task1():
    task(check_sym)


def task2():
    task(check_sym2)
