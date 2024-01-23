import numpy as np

from tools import get_lines, get_path

fn = "i.txt"


def load_board() -> np.array:
    ret = []
    for line in get_lines(get_path() + fn):
        ret.append([])
        for ch in line:
            ret[-1].append(ch == "#")
    return np.array(ret, int)


# -1: 0:-1 -> 1:
# 1: 1: -> 0:-1
def step(b: np.array) -> np.array:
    ranges = {
        -1: slice(0, -1),
        0: slice(0, None),
        1: slice(1, None),
    }
    sums = np.zeros(b.shape, int)
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            if dx == 0 and dy == 0:
                continue
            sums[ranges[dy], ranges[dx]] += b[ranges[-dy], ranges[-dx]]
    ret = np.zeros(b.shape, int)
    ret[sums == 3] = 1
    ret[(sums == 2) & (b == 1)] = 1
    return ret


def task1():
    b = load_board()
    print(b)
    for _ in range(100):
        b = step(b)
    print(b)
    print(np.sum(b))


def task2():
    b = load_board()
    b[0, 0] = 1
    b[-1, 0] = 1
    b[0, -1] = 1
    b[-1, -1] = 1
    print(b)
    for _ in range(100):
        b = step(b)
        b[0, 0] = 1
        b[-1, 0] = 1
        b[0, -1] = 1
        b[-1, -1] = 1
    print(b)
    print(np.sum(b))
