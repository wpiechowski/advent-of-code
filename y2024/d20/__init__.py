from tools import *
import numpy as np


def load(fn: str):
    lines = []
    start = 0, 0
    end = 0,0
    for y, line in enumerate(get_lines(fn)):
        data = []
        for x, ch in enumerate(line):
            data.append(1 if ch == "#" else 0)
            if ch == "S":
                start = y, x
            elif ch == "E":
                end = y, x
        lines.append(data)
    return np.array(lines, dtype=int), start, end


def find_path(maze: np.array, start: tuple[int, int], end: tuple[int, int]) -> np.array:
    path = np.zeros_like(maze)
    pts = deque([(start[0], start[1], 1)])
    while pts:
        y, x, d = pts.popleft()
        if path[y, x]:
            continue
        path[y, x] = d
        if (y, x) == end:
            break
        for dy, dx, *_ in directions:
            py, px = y + dy, x + dx
            if maze[py, px]:
                continue
            if path[py, px]:
                continue
            pts.append((py, px, d + 1))
    return path


def test_cheat(maze: np.array, path: np.array, y: int, x: int) -> int:
    vals = []
    for dy, dx in ((0, -1), (0, 1), (-1, 0), (1, 0)):
        py, px = y + dy, x + dx
        if not maze[py, px]:
            vals.append(path[py, px])
    if len(vals) < 2:
        return 0
    return max(vals) - min(vals) - 2


def print_cheat(path: np.array, p1, p2):
    for y, line in enumerate(path):
        txt = ""
        for x, val in enumerate(line):
            pp = (y, x) in (p1, p2)
            s = ("[" if pp else " ") + (f"{val:2}" if val else "  ") + ("]" if pp else " ")
            txt += s
        print(txt)


def test_cheat2(maze: np.array, path: np.array, y: int, x: int) -> Counter:
    r = 20
    cnt = Counter()
    for dy in range(-r, r + 1):
        py = y + dy
        if py >= maze.shape[0] - 1:
            continue
        if py < 1:
            continue
        for dx in range(-r, r + 1):
            c = abs(dy) + abs(dx)
            if c > r:
                continue
            px = x + dx
            if px >= maze.shape[1] - 1:
                continue
            if px < 1:
                continue
            if maze[py, px]:
                continue
            v = int(path[py, px] - path[y, x])
            d = v - c
            if d > 0:
                cnt.update([d])
            # if d == 70:
            #     print(f"{(y, x)}->{(py, px)} {c=} {v=} {d=}")
            #     print_cheat(path, (y, x), (py, px))
    return cnt


def task2():
    maze, start, end = load("i.txt")
    path = find_path(maze, start, end)
    # print(np.sum(maze) + np.sum(path>0), maze.shape[0] * maze.shape[1])
    long = np.max(path)
    print(long)
    c = Counter()
    # cc = test_cheat2(maze, path, *start)
    for y in range(1, maze.shape[0] - 1):
        for x in range(1, maze.shape[1] - 1):
            if not maze[y, x]:
                d = test_cheat2(maze, path, y, x)
                if d:
                    c += d
    ret = 0
    for k, c in sorted(c.items()):
        # print(f"{k}: {c}")
        if k >= 100:
            ret += c
    print(ret)
