from tools import *


def task1():
    mul = re.compile(r"mul\((\d+),(\d+)\)")
    ret = 0
    for line in get_lines("i.txt"):
        for m in mul.finditer(line):
            m = int(m[1]) * int(m[2])
            ret += m
    print(ret)


def task2():
    mul = re.compile(r"mul\((\d+),(\d+)\)|do\(\)|don't\(\)")
    ret = 0
    enabled = True
    for line in get_lines("i.txt"):
        for m in mul.finditer(line):
            if m[0] == "do()":
                enabled = True
            elif m[0] == "don't()":
                enabled = False
            elif enabled:
                m = int(m[1]) * int(m[2])
                ret += m
            # print(m[0])
    print(ret)
