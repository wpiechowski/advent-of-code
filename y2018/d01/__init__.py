from tools import *


def task1():
    s = 0
    for line in get_int_lines("i.txt"):
        s += sum(line)
    ic(s)


def task2():
    vals = [x[0] for x in get_int_lines("i.txt")]
    f = 0
    found = {f}
    for i, v in enumerate(cycle(vals)):
        f += v
        if f in found:
            ic(i, v, f)
            break
        found.add(f)
