import numpy as np
import pylab as plt
import re


def load_path(fn):
    x, y = 0, 0
    dirs = {
        "R": (1, 0),
        "L": (-1, 0),
        "U": (0, 1),
        "D": (0, -1),
    }
    pts = [(0, 0)]
    re_line = re.compile(r"([A-Z]) (\d+) \(#([0-9a-f]+)\)")
    for line in open(fn):
        m = re_line.match(line.strip())
        if m:
            dx, dy = dirs[m[1]]
            cnt = int(m[2])
            rgb = int(m[3], 16)
            x += dx * cnt
            y += dy * cnt
            pts.append((y, x))
    return pts


def load_path2(fn):
    x, y = 0, 0
    dirs = {
        "0": (1, 0),
        "2": (-1, 0),
        "3": (0, 1),
        "1": (0, -1),
    }
    pts = [(0, 0)]
    re_line = re.compile(r"([A-Z]) (\d+) \(#([0-9a-f]{5})([0-3])\)")
    for line in open(fn):
        m = re_line.match(line.strip())
        if m:
            dx, dy = dirs[m[4]]
            cnt = int(m[3], 16)
            x += dx * cnt
            y += dy * cnt
            pts.append((y, x))
    return pts


def plot_path(area: np.array, pts: np.array):
    y, x = pts[0, :]
    for ny, nx in pts:
        while (x, y) != (nx, ny):
            x += np.sign(nx - x)
            y += np.sign(ny - y)
            area[y, x] = 1


def flood_fill(area: np.array, y: int, x: int):
    stack = [(y, x)]
    while stack:
        y, x = stack.pop()
        for dy, dx in ((0, -1), (0, 1), (-1, 0), (1, 0)):
            if area[y + dy, x + dx]:
                continue
            area[y + dy, x + dx] = 1
            stack.append((y + dy, x + dx))


def count_fill(area: np.array) -> int:
    s = np.sum(area)
    return s


def task1():
    fn = "i18a.txt"
    pts = load_path(fn)
    pts = np.array(pts)
    pts[:, 0] -= np.min(pts[:, 0])
    pts[:, 1] -= np.min(pts[:, 1])
    mx = np.max(pts[:, 1])
    my = np.max(pts[:, 0])
    print(mx, my)
    area = np.zeros((my + 1, mx + 1), dtype=int)
    plot_path(area, pts)
    flood_fill(area, 300, 100)
    print(count_fill(area))
    fig, ax = plt.subplots()
    # ax.plot(pts[:, 1], pts[:, 0])
    plt.imshow(area)
    ax.axis("equal")
    plt.show()


def triangle(x1: int, y1: int, x2: int, y2: int) -> int:
    p = x1 * y2 - x2 * y1
    return abs(p)


def calc_area(pts: list[tuple[int, int]]) -> int:
    area = 0
    y0, x0 = pts[0]
    for n in range(0, len(pts) - 0):
        p1 = pts[n]
        p1 = p1[0] - y0, p1[1] - x0
        p2 = pts[(n + 1) % len(pts)]
        p2 = p2[0] - y0, p2[1] - x0
        a = triangle(p1[1], p1[0], p2[1], p2[0])
        c1 = complex(p1[1], p1[0])
        c2 = complex(p2[1], p2[0])
        if a and ((c2 - c1) / c1).imag > 0:
            area -= a
        else:
            area += a
        area += abs(p1[1] - p2[1]) + abs(p1[0] - p2[0])
        print(p1, p2, a)
    return area


def task2():
    fn = "i18a.txt"
    pts = load_path2(fn)
    # pts = np.array(pts, dtype=int)
    a = calc_area(pts) // 2
    print(a)
    # fig, ax = plt.subplots()
    # ax.plot(pts[:, 1], pts[:, 0])
    # ax.axis("equal")
    # plt.show()
