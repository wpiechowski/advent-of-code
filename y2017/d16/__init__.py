import re

from tools import *


def process(line: str):
    code = "abcdefghijklmnop"
    rx = re.compile(r"([sxp])([0-9a-z]+)(/([0-9a-z]+))?")
    hist = set()
    for k in range(1000):
        ic(k, code)
        if code in hist:
            break
        hist.add(code)
        for item in rx.finditer(line):
            oper, a1, a2 = item.group(1, 2, 4)
            if oper == "s":
                p = int(a1)
                code = code[-p:] + code[:-p]
            else:
                if oper == "p":
                    a1 = code.find(a1)
                    a2 = code.find(a2)
                p1, p2 = min_max((int(a1), int(a2)))
                code = code[:p1] + code[p2] + code[p1 + 1: p2] + code[p1] + code[p2 + 1:]
    ic(code)


def task1():
    for line in get_lines("i.txt"):
        process(line)
