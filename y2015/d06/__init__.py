import re
import numpy as np


re_line = re.compile(r"(toggle|turn on|turn off) (\d+),(\d+) through (\d+),(\d+)")


def parse_line(line: str):
    m = re_line.match(line)
    return m[1], int(m[2]), int(m[3]), int(m[4]), int(m[5])


def task1():
    fn = "y2015/d06/i.txt"
    data = np.zeros((1000, 1000), int)
    for line in open(fn):
        vals = parse_line(line.strip())
        print(vals)
        sub = data[vals[1]: vals[3] + 1, vals[2]: vals[4] + 1]
        if vals[0] == "turn on":
            sub[:, :] = 1
        elif vals[0] == "turn off":
            sub[:, :] = 0
        else:
            sub[:, :] = 1 - sub[:, :]
    print(np.sum(data))


def task2():
    fn = "y2015/d06/i.txt"
    data = np.zeros((1000, 1000), int)
    for line in open(fn):
        vals = parse_line(line.strip())
        print(vals)
        sub = data[vals[1]: vals[3] + 1, vals[2]: vals[4] + 1]
        if vals[0] == "turn on":
            sub[:, :] += 1
        elif vals[0] == "turn off":
            sub[:, :] -= 1
            sub[sub < 0] = 0
        else:
            sub[:, :] += 2
    print(np.sum(data))
