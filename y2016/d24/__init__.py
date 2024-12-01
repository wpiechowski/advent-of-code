from collections import deque
from itertools import permutations

from tools import get_lines, directions
import numpy as np


def load_maze():
    fn = "i.txt"
    maze = []
    points = {}
    for y, line in enumerate(get_lines(fn)):
        maze_line = []
        for x, ch in enumerate(line):
            if ch == "#":
                maze_line.append(1)
            else:
                maze_line.append(0)
            if ch in "0123456789":
                points[int(ch)] = y, x
        maze.append(maze_line)
    return np.array(maze), points


def find_distance(maze: np.array, p1: tuple[int, int], p2: tuple[int, int]) -> int:
    steps = np.zeros(maze.shape, int)
    q = deque([(p1, 1)])
    while q:
        p1, moves = q.popleft()
        if steps[p1]:
            continue
        if p1 == p2:
            return moves - 1
        steps[p1] = moves
        for dy, dx, _ in directions:
            p = p1[0] + dy, p1[1] + dx
            if maze[p]:
                continue
            if steps[p]:
                continue
            q.append((p, moves + 1))


def calc_graph(maze: np.array, points: dict[int, tuple[int, int]]) -> np.array:
    dist = np.zeros((len(points), len(points)), int)
    for n1, pos1 in points.items():
        for n2, pos2 in points.items():
            dist[n1, n2] = find_distance(maze, pos1, pos2)
    return dist


def find_shortest_path(dist: np.array):
    best = None
    for path in permutations(range(1, dist.shape[0])):
        cur_pos = 0
        cur_len = 0
        for pt in path:
            cur_len += dist[cur_pos, pt]
            cur_pos = pt
        # part 2:
        cur_len += dist[cur_pos, 0]
        if best is None or cur_len < best[0]:
            best = cur_len, path
    return best


def task1():
    maze, points = load_maze()
    ic(points)
    graph = calc_graph(maze, points)
    ic(graph)
    path_len = find_shortest_path(graph)
    ic(path_len)
