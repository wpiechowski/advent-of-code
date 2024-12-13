from collections import defaultdict
from dataclasses import field

from tools import *
import numpy as np


def load(fn: str) -> np.array:
    data = []
    for line in get_lines(fn):
        cur = [ord(x) for x in line]
        data.append(cur)
    z = np.zeros((len(data) + 2, len(data[0]) + 2), dtype=int)
    z[1: 1 + len(data), 1: 1 + len(data[0])] = data
    return z


def fill_area(arr: np.array, ret: np.array, y: int, x: int, name: int):
    val = arr[y, x]
    ret[y, x] = name
    for dy, dx, *_ in directions:
        py, px = y + dy, x + dx
        if ret[py, px] or arr[py, px] != val:
            continue
        fill_area(arr, ret, py, px, name)


def rename(arr: np.array) -> np.array:
    ret = np.zeros_like(arr)
    name = 1
    for y in range(1, arr.shape[0] - 1):
        for x in range(1, arr.shape[1] - 1):
            if ret[y, x] == 0:
                fill_area(arr, ret, y, x, name)
                name += 1
    return ret


@dataclass
class Plot:
    area: int = 0
    perimeter: int = 0
    edges: set = field(default_factory=set)

    def calc_sides(self):
        found = 0
        edges = list(self.edges)
        while edges:
            y, x, dy, dx = edges.pop()
            found += 1
            if dy:
                # horz
                xx = x + 1
                while (y, xx, dy, dx) in edges:
                    edges.remove((y, xx, dy, dx))
                    xx += 1
                xx = x - 1
                while (y, xx, dy, dx) in edges:
                    edges.remove((y, xx, dy, dx))
                    xx -= 1
            else:
                # vert
                yy = y + 1
                while (yy, x, dy, dx) in edges:
                    edges.remove((yy, x, dy, dx))
                    yy += 1
                yy = y - 1
                while (yy, x, dy, dx) in edges:
                    edges.remove((yy, x, dy, dx))
                    yy -= 1
        return found


def task1():
    arr = load("i.txt")
    arr = rename(arr)
    data = defaultdict(Plot)
    for y in range(1, arr.shape[0] - 1):
        for x in range(1, arr.shape[1] - 1):
            cur = arr[y, x]
            data[cur].area += 1
            for dy, dx, *_ in directions:
                if arr[y + dy, x + dx] != cur:
                    data[cur].perimeter += 1
    price = 0
    for k, v in data.items():
        print(k, v)
        price += v.area * v.perimeter
    print(price)


def task2():
    arr = load("i.txt")
    arr = rename(arr)
    data = defaultdict(Plot)
    for y in range(1, arr.shape[0] - 1):
        for x in range(1, arr.shape[1] - 1):
            cur = arr[y, x]
            data[cur].area += 1
            for dy, dx, *_ in directions:
                if arr[y + dy, x + dx] != cur:
                    data[cur].edges.add((y, x, dy, dx))
    price = 0
    for k, v in data.items():
        sides = v.calc_sides()
        print(k, v.area, sides)
        price += v.area * sides
    print(price)
