import numpy as np


def load_board(fn: str) -> np.array:
    lines = []
    for line in open(fn):
        l = []
        for ch in line.strip():
            if ch == ".":
                val = 0
            elif ch == "O":
                val = 1
            elif ch == "#":
                val = 2
            l.append(val)
        lines.append(l)
    return np.array(lines)


def tilt_col(col: np.array, out: np.array):
    free = 0
    for x, v in enumerate(col):
        if v == 2:
            free = x + 1
            out[x] = 2
        elif v == 1:
            out[x] = 0
            out[free] = 1
            free += 1
        else:
            out[x] = 0


def tilt_up(b: np.array) -> np.array:
    out = np.zeros(b.shape, dtype=int)
    for col, out_col in zip(b.T, out.T):
        tilt_col(col, out_col)
    return out


def calc_weight(b: np.array) -> int:
    ret = 0
    for n, line in enumerate(b):
        s = np.sum(line == 1)
        ret += s * (b.shape[0] - n)
    return ret


def tilt_cycle(b: np.array) -> np.array:
    ret = b.copy()
    for _ in range(4):
        ret = tilt_up(ret)
        ret = np.rot90(ret, 3)
    return ret

def line_to_str(l: np.array) -> str:
    txt = ""
    for v in l:
        if v == 0:
            txt += "."
        elif v == 1:
            txt += "O"
        else:
            txt += "#"
    return txt


def to_str(b: np.array):
    lines = map(line_to_str, b)
    return "\n".join(lines)


def task1():
    fn = "i14s.txt"
    b = load_board(fn)
    # print(b)
    b2 = b * 0
    tilt_up(b, b2)
    print(b2)
    ret = calc_weight(b2)
    print(ret)


def task2():
    fn = "i14a.txt"
    b = load_board(fn)
    # print(b)
    cache = {}
    b2 = b * 1
    for n in range(1000000000):
        s = to_str(b)
        if s in cache:
            prev_n = cache[s]
            print(f"cache hit {n=}, {prev_n}")
            break
        else:
            cache[s] = n
        b = tilt_cycle(b)
    k = (1000000000 - prev_n) % (n - prev_n) + prev_n
    for _ in range(k):
        b2 = tilt_cycle(b2)
    # print(to_str(b2))
    ret = calc_weight(b2)
    print(ret)
