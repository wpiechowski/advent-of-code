import re

from tools import get_lines

fn = "i.txt"
re_marker = re.compile(r"\((\d+)x(\d+)\)")


def task1():
    for line in get_lines(fn):
        pos = 0
        txt = ""
        while m := re_marker.search(line[pos:]):
            ic(m.groups())
            rep = int(m[2])
            size = int(m[1])
            txt += line[pos: m.start() + pos]
            rep_str = line[pos + m.end(): pos + m.end() + size]
            txt += rep_str * rep
            pos += m.end() + size
        txt += line[pos:]
        ic(len(txt))


def calc_len(s: str) -> int:
    m = re_marker.search(s)
    if not m:
        return len(s)
    rep_len = int(m[1])
    rep_count = int(m[2])
    sub_str = s[m.end(): m.end() + rep_len]
    sub_len = calc_len(sub_str)
    tail = s[m.end() + rep_len:]
    tail_len = calc_len(tail)
    return m.start() + rep_count * sub_len + tail_len


def task2():
    for line in get_lines(fn):
        l = calc_len(line)
        ic(l)
