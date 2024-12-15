from tools import *
import numpy as np


def load(fn: str):
    maze = []
    codes = {
        ".": 0,
        "#": 1,
        "O": 2,
        "@": 0,
    }
    pos = 0, 0
    moves = ""
    for line in get_lines(fn):
        if "#" in line:
            if "@" in line:
                pos = len(maze), line.find("@")
            maze.append([codes[x] for x in line])
        elif line:
            moves += line
    return np.array(maze, dtype=int), pos, moves


def try_move(maze: np.array, y: int, x: int, dy: int, dx: int) -> bool:
    if maze[y, x] == 0:
        return True
    elif maze[y, x] == 1:
        return False
    elif maze[y, x] == 2:
        b = try_move(maze, y + dy, x + dx, dy, dx)
        if b:
            maze[y + dy, x + dx] = 2
            maze[y, x] = 0
        return b
    raise ValueError("bad code")


def pr(maze: np.array, y: int, x: int):
    codes = ".#O@"
    maze[y, x] = 3
    for line in maze:
        print("".join([codes[x] for x in line]))
    maze[y, x] = 0


def calc_score(maze: np.array) -> int:
    score = 0
    for y, line in enumerate(maze):
        for x, val in enumerate(line):
            if val == 2:
                score += 100 * y + x
    return score


def task1():
    fn = "i.txt"
    maze, (y, x), moves = load(fn)
    pr(maze, y, x)
    print(y, x, len(moves))
    dirs = {d[3]: (d[0], d[1]) for d in directions}
    for m in moves:
        dy, dx = dirs[m]
        py = y + dy
        px = x + dx
        b = try_move(maze, py, px, dy, dx)
        if b:
            y, x = py, px
    # print(m)
    pr(maze, y, x)
    print(calc_score(maze))
