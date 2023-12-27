import numpy as np
import pylab as plt


class Cell:
    def __init__(self, x: int, y: int, joints: str):
        self.x = x
        self.y = y
        self.neighs = set()
        self.start = joints == "S"
        self.joint = joints
        if joints in "-J7":
            self.neighs.add((x - 1, y))
        if joints in "-LF":
            self.neighs.add((x + 1, y))
        if joints in "|LJ":
            self.neighs.add((x, y - 1))
        if joints in "|7F":
            self.neighs.add((x, y + 1))

    def other(self, x, y) -> tuple[int, int]:
        ss = self.neighs - {(x, y)}
        if len(ss) != 1:
            raise ValueError(f"{x} {y} not here: {self.x} {self.y})")
        ret = list(ss)[0]
        if ret == (x, y):
            raise ValueError("sdfgsd")
        return ret

    def __str__(self):
        return self.joint

    def __repr__(self):
        return f"Cell({self.x}, {self.y}, {self.neighs}, {self.joint}"


def load_maze(fn):
    lines = []
    for y, line in enumerate(open(fn)):
        lines.append([])
        for x, ch in enumerate(line.strip()):
            lines[-1].append(Cell(x, y, ch))
            if ch == "S":
                xs = x
                ys = y
    return lines, xs, ys


def find_loop(lines, xs, ys, dx, dy):
    ret = []
    x = xs
    y = ys
    # print(f"start {x} {y}")
    c = lines[ys + dx][xs + dy]
    ret.append((c.x, c.y))
    if (xs, ys) not in c.neighs:
        return []
    while True:
        ox, oy = c.other(x, y)
        # print(f"{c.x} {c.y} -> {c.joint} {ox} {oy}")
        if ox < 0 or ox >= len(lines[0]):
            return []
        if oy < 0 or oy >= len(lines):
            return []
        cc = lines[oy][ox]
        if (ox, oy) == (xs, ys):
            ret.append((ox, oy))
            return ret
        if (c.x, c.y) not in cc.neighs:
            return []
        if (ox, oy) in ret:
            return []
        ret.append((ox, oy))
        x, y = c.x, c.y
        c = cc


def angle(px, py):
    ret = (px > 0) + 2 * (py > 0)
    if ret == 2:
        ret = 3
    elif ret == 3:
        ret = 2
    return ret


def check_point(loop, px: int, py: int):
    a = angle(loop[0][0] - px, loop[0][1] - py)
    ca = 0
    # print("start", px, py)
    for x, y in loop:
        na = angle(x - px, y - py)
        da = na - a
        if da < -2:
            da += 4
        if da > 2:
            da -= 4
        a = na
        ca += da
        # print(f"{x=} {y=} {x - px} {y - py} {na=} {da=} {ca=}")
    print(px, py, ca)
    return abs(ca) >= 2


def task2(sy: int, sx: int, loop: list[tuple[int, int]]):
    # loop = np.array(loop)
    vals = np.zeros((sy, sx), dtype=int)
    for x, y in loop:
        vals[y, x] = 2
    score = 0
    for py in range(sy):
        for px in range(sx):
            if vals[py, px] == 2:
                continue
            v = check_point(loop, px, py)
            vals[py, px] = v
            score += v
    plt.imshow(vals)
    plt.show()
    print(score)


def task1():
    lines, xs, ys = load_maze("i10a.txt")
    # list(map(print, "".join(map(str, lines))))
    # print(xs, ys)
    for dx, dy in ((-1, 0), (0, -1), (1, 0), (0, 1)):
        l = find_loop(lines, xs, ys, dx, dy)
        if l:
            # print(l)
            print(len(l), (len(l)) / 2, len(lines) * len(lines[0]))
            break
    # l.append((xs, ys))
    task2(len(lines), len(lines[0]), l)
