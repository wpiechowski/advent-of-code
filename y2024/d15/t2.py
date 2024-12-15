from tools import *
import numpy as np


inv_codes = ".#[]O@"
codes = {ch: pos for pos, ch in enumerate(inv_codes)}


def load(fn: str):
    maze = []
    pos = 0, 0
    moves = ""
    for line in get_lines(fn):
        if "#" in line:
            if "@" in line:
                pos = len(maze), line.find("@") * 2
            cur = []
            for ch in line:
                if ch in ".@":
                    cur.extend([0, 0])
                elif ch == "#":
                    cur.extend([1, 1])
                elif ch == "O":
                    cur.extend([2, 3])
            maze.append(cur)
        elif line:
            moves += line
    return np.array(maze, dtype=int), pos, moves


def pr(maze: np.array, y: int, x: int):
    maze[y, x] = 5
    for line in maze:
        print("".join([inv_codes[x] for x in line]))
    maze[y, x] = 0


def calc_score(maze: np.array) -> int:
    score = 0
    for y, line in enumerate(maze):
        for x, val in enumerate(line):
            if val == 2:
                score += 100 * y + x
    return score


def try_move(maze: np.array, y: int, x: int, dy: int, dx: int) -> bool:
    if maze[y, x] == 0:
        return True
    elif maze[y, x] == 1:
        return False
    elif maze[y, x] in (2, 3):
        if dx:
            b = try_move(maze, y + dy, x + dx, dy, dx)
            if b:
                maze[y + dy, x + dx] = maze[y, x]
                maze[y, x] = 0
        else:
            if maze[y, x] == 2:
                pl = y, x
                pr = y, x + 1
            else:
                pl = y, x - 1
                pr = y, x
            mc = maze.copy()
            b = try_move(mc, pl[0] + dy, pl[1] + dx, dy, dx)
            if b:
                b = try_move(mc, pr[0] + dy, pr[1] + dx, dy, dx)
                if b:
                    maze[:, :] = mc
                    maze[pl[0] + dy, pl[1] + dx] = 2
                    maze[pr[0] + dy, pr[1] + dx] = 3
                    maze[pl] = 0
                    maze[pr] = 0
        return b
    raise ValueError("bad code")


def task2():
    dirs = {d[3]: (d[0], d[1]) for d in directions}
    maze, (y, x), moves = load("i.txt")
    pr(maze, y, x)
    print(y, x)
    for m in moves:
        dy, dx = dirs[m]
        py = y + dy
        px = x + dx
        b = try_move(maze, py, px, dy, dx)
        if b:
            y, x = py, px
        # print(m)
        # pr(maze, y, x)
    # print(m)
    pr(maze, y, x)
    print(calc_score(maze))
