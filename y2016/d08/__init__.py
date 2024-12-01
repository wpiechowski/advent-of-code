import re

import numpy as np

from tools import get_lines

fn = "i.txt"
dim = 6, 50


def display(disp: np.array):
    for line in disp:
        txt = "".join(".#"[x] for x in line)
        print(txt)


def task1():
    re_rect = re.compile(r"rect (\d+)x(\d+)")
    re_rotc = re.compile(r"rotate column x=(\d+) by (\d+)")
    re_rotr = re.compile(r"rotate row y=(\d+) by (\d+)")
    disp = np.zeros(dim, int)
    for line in get_lines(fn):
        if m := re_rect.match(line):
            x, y = int(m[1]), int(m[2])
            disp[:y, :x] = 1
        elif m := re_rotc.match(line):
            col, cnt = int(m[1]), int(m[2])
            for _ in range(cnt):
                tmp = disp[-1, col]
                disp[1:, col] = disp[:-1, col]
                disp[0, col] = tmp
        elif m := re_rotr.match(line):
            row, cnt = int(m[1]), int(m[2])
            for _ in range(cnt):
                tmp = disp[row, -1]
                disp[row, 1:] = disp[row, :-1]
                disp[row, 0] = tmp
        print(line)
        display(disp)
    print(np.sum(disp))
