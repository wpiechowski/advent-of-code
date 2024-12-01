import inspect
import re
from icecream import ic
import time
from itertools import cycle, product
from collections import Counter, deque
from dataclasses import dataclass


directions = (
    (0, 1, "R"),
    (0, -1, "L"),
    (1, 0, "D"),
    (-1, 0, "U"),
)


def get_path():
    re_path = re.compile(r"y(\d{4})\\d(\d{2})\\")
    stack = inspect.stack()
    for entry in stack:
        f = entry.filename
        for m in re_path.finditer(f):
            return m[0]
    return ""


def get_lines(fn: str, strip=True):
    for line in open(get_path() + fn):
        if strip:
            yield line.strip()
        else:
            yield line


def get_re_lines(fn: str, rx: str):
    re_line = re.compile(rx)
    for line in get_lines(fn):
        m = re_line.match(line)
        if m:
            yield m.groups()


def row_of_ints(line: str) -> list[int]:
    return list(map(lambda x: int(x[0]), re.finditer(r"[+\-]?\d+", line)))


def get_int_lines(fn: str):
    for line in get_lines(fn):
        yield row_of_ints(line)


def min_max(a) -> tuple:
    return min(a), max(a)


def test():
    get_path()


if __name__ == "__main__":
    test()
