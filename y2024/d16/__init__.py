import heapq

from tools import *
import numpy as np


def load(fn: str):
    lines = []
    start = 0, 0
    end = 0,0
    for y, line in enumerate(get_lines(fn)):
        data = []
        for x, ch in enumerate(line):
            data.append(-1 if ch == "#" else 0)
            if ch == "S":
                start = y, x
            elif ch == "E":
                end = y, x
        lines.append(data)
    return np.array(lines, dtype=int), start, end


@dataclass(order=True)
class State:
    score: int
    y: int
    x: int
    head: int
    prev_state: object = None


def task1():
    maze, start, end = load("i1.txt")
    cache = {}
    paths = [State(0, start[0], start[1], 0)]
    heapq.heapify(paths)
    while state := heapq.heappop(paths):
        state.head %= 4
        if (state.y, state.x) == end:
            print(state.score)
            break
        if maze[state.y, state.x] < 0:
            continue
        key = state.y, state.x, state.head
        if key in cache:
            continue
        cache[key] = state.score
        d = directions[state.head]
        heapq.heappush(paths, State(state.score + 1, state.y + d[0], state.x + d[1], state.head))
        heapq.heappush(paths, State(state.score + 1000, state.y, state.x, state.head + 1))
        heapq.heappush(paths, State(state.score + 1000, state.y, state.x, state.head - 1))


def add_path(seats: np.array, state: State):
    if state:
        seats[state.y, state.x] = 1
        for p in state.prev_state:
            add_path(seats, p)


def task2():
    maze, start, end = load("i.txt")
    cache = {}
    paths = [State(0, start[0], start[1], 0, [])]
    best_score = 0
    seats = np.zeros_like(maze)
    heapq.heapify(paths)
    while state := heapq.heappop(paths):
        state.head %= 4
        if (state.y, state.x) == end:
            print(state.score)
            if not best_score:
                best_score = state.score
            if state.score > best_score:
                break
            add_path(seats, state)
            continue
        if maze[state.y, state.x] < 0:
            continue
        key = state.y, state.x, state.head
        if key in cache:
            if cache[key].score == state.score:
                cache[key].prev_state.append(state)
            continue
        cache[key] = state
        d = directions[state.head]
        heapq.heappush(paths, State(state.score + 1, state.y + d[0], state.x + d[1], state.head, [state]))
        heapq.heappush(paths, State(state.score + 1000, state.y, state.x, state.head + 1, [state]))
        heapq.heappush(paths, State(state.score + 1000, state.y, state.x, state.head - 1, [state]))
    print(seats)
    print(np.sum(seats))
