from tools import *


def can_do(target: int, vals: list[int]) -> bool:
    for i in range(2 ** (len(vals)-1)):
        val = vals[0]
        for k in range(1, len(vals)):
            v = vals[k]
            if i & (1 << (k-1)):
                val *= v
            else:
                val += v
        if val == target:
            return True
    return False


def task1():
    ret = 0
    for line in get_int_lines("i.txt"):
        target = line[0]
        vals = line[1:]
        if can_do(target, vals):
            ret += target
    print(ret)


def can_do2(target: int, vals: list[int]) -> bool:
    for opers in product("+*|", repeat=len(vals)-1):
        val = vals[0]
        for oper, v in zip(opers, vals[1:]):
            if oper == "+":
                val += v
            elif oper == "*":
                val *= v
            else:
                val = int(str(val) + str(v))
        if val == target:
            return True
    return False


def task2():
    ret = 0
    for line in get_int_lines("i.txt"):
        target = line[0]
        vals = line[1:]
        print(line)
        if can_do2(target, vals):
            ret += target
    print(ret)
