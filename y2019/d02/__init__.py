from tools import *


def sim(code: list[int]) -> int:
    for pc in range(0, len(code), 4):
        op = code[pc]
        v1 = code[code[pc+1]]
        v2 = code[code[pc+2]]
        res = code[pc+3]
        if op == 1:
            o = v1 + v2
        elif op == 2:
            o = v1 * v2
        else:
            break
        code[res] = o
    return code[0]


def task1():
    code = list(get_int_lines("i.txt"))[0]
    code[1] = 12
    code[2] = 2
    ret = sim(code)
    print(ret)


def task2():
    code = list(get_int_lines("i.txt"))[0]
    for n in range(100):
        for v in range(100):
            c = code.copy()
            c[1] = n
            c[2] = v
            res = sim(c)
            if res == 19690720:
                print(n, v)
                return
