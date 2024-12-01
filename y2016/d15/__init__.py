from math import lcm

from tools import get_re_lines

fn = "i2.txt"
re_line = r"Disc #(\d+) has (\d+) positions; at time=(\d+), it is at position (\d+)"


def load():
    ret = []
    for vals in get_re_lines(fn, re_line):
        dn, counts, t0, pos = tuple(map(int, vals))
        pos = (pos + dn - t0) % counts
        ret.append((counts, pos))
    return ret


def task1():
    data = load()
    print(data)
    period = 1
    offset = 0
    for counts, pos in data:
        for n in range(counts):
            x = offset + n * period
            if (x + pos) % counts == 0:
                period = lcm(period, counts)
                offset = x
                ic(period, offset, n)
                break
