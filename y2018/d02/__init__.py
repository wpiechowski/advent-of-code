from tools import *


def task1():
    n2 = 0
    n3 = 0
    for line in get_lines("i.txt"):
        c = Counter(line)
        for _, cnt in c.items():
            if cnt == 2:
                n2 += 1
                break
        for _, cnt in c.items():
            if cnt == 3:
                n3 += 1
                break
    ic(n2, n3, n2 * n3)


def task2():
    lines = list(get_lines("i.txt"))
    for w1, w2 in product(lines, lines):
        dif = 0
        for n, (c1, c2) in enumerate(zip(w1, w2)):
            if c1 != c2:
                dif += 1
                pos = n
        if dif == 1:
            ic(w1, w2, pos)
            return
