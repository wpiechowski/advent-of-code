from tools import *


def task1():
    ret = 0
    for line in get_lines("i.txt"):
        words = line.split(" ")
        s = set(words)
        if len(s) == len(words):
            ret += 1
    ic(ret)


def task2():
    ret = 0
    for line in get_lines("i.txt"):
        words = line.split(" ")
        words = ["".join(sorted(w)) for w in words]
        s = set(words)
        if len(s) == len(words):
            ret += 1
    ic(ret)
