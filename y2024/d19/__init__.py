from tools import *


towels = []


def load_iter(fn: str):
    global towels
    for line in get_lines(fn):
        if "," in line:
            towels = sorted(line.split(", "), key=len, reverse=True)
        elif line:
            yield line


def possible(code: str) -> bool:
    if not code:
        return True
    for t in towels:
        if len(t) > len(code):
            continue
        if code.startswith(t):
            p = possible(code[len(t):])
            if p:
                return True
    return False


def task1():
    good = 0
    for code in load_iter("i.txt"):
        print(code)
        if possible(code):
            good += 1
    print(good)


@cache
def possible2(code: str) -> int:
    if not code:
        return 1
    p = 0
    for t in towels:
        if len(t) > len(code):
            continue
        if code.startswith(t):
            p += possible2(code[len(t):])
    return p


def task2():
    good = 0
    for code in load_iter("i.txt"):
        print(code)
        good += possible2(code)
    print(good)
