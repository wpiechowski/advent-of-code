import collections

from tools import get_re_lines

fn = "i.txt"
re_line = r"([a-z\-]+)-(\d+)\[([a-z]{5})\]"


def check(name: str):
    c = collections.Counter(name.replace("-", ""))
    items = [(-cnt, val) for val, cnt in c.items()]
    items.sort()
    # print(items)
    cksum = "".join(map(lambda i: i[1], items[:5]))
    # print(cksum)
    return cksum


def task1():
    ids = 0
    for line in get_re_lines(fn, re_line):
        # print(line)
        if check(line[0]) == line[2]:
            ids += int(line[1])
    print(ids)


def shift(x: str) -> str:
    ret = ""
    for ch in x:
        if ch == "z":
            ch = "a"
        elif ch in ("-", " "):
            ch = " "
        else:
            ch = chr(ord(ch) + 1)
        ret += ch
    return ret


def task2():
    for line in get_re_lines(fn, re_line):
        if check(line[0]) == line[2] or True:
            cnt = int(line[1])
            n = line[0]
            for _ in range(cnt):
                n = shift(n)
            print(line[1], n)
