from tools import get_int_lines, min_max

fn = "i.txt"


def task1():
    ret = 0
    for vals in get_int_lines(fn):
        a, b = min_max(vals)
        ret += b - a
    print(ret)


def task2():
    ret = 0
    for vals in get_int_lines(fn):
        for a in vals:
            for b in vals:
                if a > b and a % b == 0:
                    ic(a, b)
                    ret += a // b
    ic(ret)
