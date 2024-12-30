from tools import *


def task1():
    score = 0
    for val, in get_int_lines("i.txt"):
        score += val // 3 - 2
    print(score)


def task2():
    score = 0
    for val, in get_int_lines("i.txt"):
        while True:
            val = val // 3 - 2
            if val <= 0:
                break
            score += val
    print(score)
