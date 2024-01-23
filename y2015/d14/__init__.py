from tools import get_re_lines
import pylab as plt
import numpy as np


def calc_dist(line, total):
    speed, time, rest = list(map(int, line[1:]))
    cycle = time + rest
    full = total // cycle
    frac = total % cycle
    dist = speed * (full * time + min(frac, time))
    return dist


def task1():
    r = r"(\w+) can fly (\d+) km/s for (\d+) [a-z, ]+ (\d+) .+"
    fn = "i.txt"
    total = 2503
    best = 0
    for line in get_re_lines(fn, r):
        print(line)
        d = calc_dist(line, total)
        best = max(best, d)
    print(best)


def task2():
    r = r"(\w+) can fly (\d+) km/s for (\d+) [a-z, ]+ (\d+) .+"
    fn = "i.txt"
    total = 2503
    lines = list(get_re_lines(fn, r))
    pos = np.zeros((len(lines), total), int)
    pts = np.zeros((len(lines),), int)
    for step in range(total):
        for l, line in enumerate(lines):
            pos[l, step] = calc_dist(line, step + 1)
        mx = np.max(pos[:, step])
        pts[pos[:, step] == mx] += 1
    print(pts)
    plt.plot(pos.T)
    plt.show()
