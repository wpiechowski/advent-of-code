from tools import get_re_lines


def load():
    fn = "i.txt"
    re_line = r"(\d+)-(\d+)"
    return [(int(a), int(b)) for a, b in get_re_lines(fn, re_line)]


def check(data, addr):
    for a, b in data:
        if a <= addr <= b:
            print(a, b)
            return False
    return True


def task1():
    data = load()
    data.sort()
    top = 0
    for a, b in data:
        if a > top + 1:
            ic(top + 1, a)
            break
        top = max(top, b)
    ic(check(data, top + 1))


def task2():
    data = load()
    data.sort()
    free = 0
    top = 0
    for a, b in data:
        if a > top + 1:
            ic(top + 1, a)
            free += a - top - 1
        top = max(top, b)
    ic(free)
