from tools import get_lines

fn = "i.txt"


def iter_pairs(txt: str):
    for n in range(-1, len(txt) - 1):
        if txt[n] == txt[n + 1]:
            yield int(txt[n])


def iter_pairs2(txt: str):
    l = len(txt) // 2
    for n in range(len(txt)):
        if txt[n] == txt[(n + l) % len(txt)]:
            yield int(txt[n])


def task1():
    for line in get_lines(fn):
        s = sum(iter_pairs2(line))
        print(s)
