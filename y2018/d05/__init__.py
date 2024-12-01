from tools import *


def find_pair(t: str) -> int:
    for n in range(len(t) - 1):
        c1 = ord(t[n])
        c2 = ord(t[n + 1])
        if c1 ^ c2 == 32:
            return n
    return -1


def process(t: str):
    while (n := find_pair(t)) >= 0:
        t = t[:n] + t[n + 2:]
        # ic(len(t))
    return len(t)


def task1():
    for line in get_lines("i.txt"):
        process(line)


def task2():
    for line in get_lines("i.txt"):
        best = len(line)
        for ch in "qwertyuiopasdfghjklzxcvbnm":
            t = line.replace(ch, "").replace(ch.upper(), "")
            if len(t) == len(line):
                continue
            ic("remove", ch)
            r = process(t)
            ic(r)
            best = min(r, best)
    ic(best)
