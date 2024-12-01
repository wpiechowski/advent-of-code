from tools import *


def task1():
    code = [int(line) for line in get_lines("i.txt")]
    pc = 0
    steps = 0
    while 0 <= pc < len(code):
        pc2 = pc + code[pc]
        code[pc] += 1
        pc = pc2
        steps += 1
    ic(steps)


def task2():
    code = [int(line) for line in get_lines("i.txt")]
    pc = 0
    steps = 0
    while 0 <= pc < len(code):
        pc2 = pc + code[pc]
        if code[pc] >= 3:
            code[pc] -= 1
        else:
            code[pc] += 1
        pc = pc2
        steps += 1
    ic(steps)
