from tools import *


def load(fn: str):
    ants = {}
    size_y = size_x = 0
    for y, line in enumerate(get_lines(fn)):
        for x, ch in enumerate(line):
            size_x = x + 1
            if ch == ".":
                continue
            if ch not in ants:
                ants[ch] = []
            ants[ch].append((y, x))
        size_y = y + 1
    return (size_y, size_x), ants


def task1():
    size, ants = load("i.txt")
    print(size)
    # for k, v in ants.items():
    #     ic(k, v)
    pts = set()
    for name, locs in ants.items():
        print(name, locs)
        for p1, p2 in combinations(locs, 2):
            dy = p2[0] - p1[0]
            dx = p2[1] - p1[1]
            for py, px in zip((p1[0] - dy, p2[0] + dy), (p1[1] - dx, p2[1] + dx)):
                # print(p1, p2, py, px)
                if not (0 <= py < size[0]) or not (0 <= px < size[1]):
                    continue
                pts.add((py, px))
    # print(pts)
    print(len(pts))


def task2():
    size, ants = load("i.txt")
    print(size)
    # for k, v in ants.items():
    #     ic(k, v)
    pts = set()
    for name, locs in ants.items():
        print(name, locs)
        for p1, p2 in permutations(locs, 2):
            dy = p2[0] - p1[0]
            dx = p2[1] - p1[1]
            py, px = p1
            while True:
                if not (0 <= py < size[0]) or not (0 <= px < size[1]):
                    break
                pts.add((py, px))
                py -= dy
                px -= dx
    # print(pts)
    print(len(pts))
