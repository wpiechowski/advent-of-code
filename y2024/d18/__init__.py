from tools import *
import numpy as np


def load(fn: str, size: int) -> np.array:
    arr = np.zeros((size, size), dtype=int)
    for n, (x, y) in enumerate(get_int_lines(fn)):
        arr[y, x] = n + 1
    return arr


def task1():
    # fn, size, limit = "i1.txt", 7, 12
    fn, size, limit = "i.txt", 71, 1024
    area = load(fn, size)
    print(find_path(area, limit))


def find_path(area: np.array, limit: int) -> int:
    start = (0, 0)
    size = area.shape[0]
    end = (size-1, size-1)
    q = deque([(start[0], start[1], 1)])
    steps = np.zeros_like(area)
    # print(area)
    while q:
        y, x, dist = q.popleft()
        if steps[y, x]:
            continue
        if 0 < area[y, x] <= limit:
            continue
        steps[y, x] = dist
        if (y, x) == end:
            # print(steps)
            return dist - 1
        for dy, dx, *_ in directions:
            py = y + dy
            px = x + dx
            if not (0 <= py < size) or not (0 <= px < size):
                continue
            q.append((py, px, dist + 1))
    return 0


def task2():
    # fn, size, limit = "i1.txt", 7, 12
    fn, size, limit = "i.txt", 71, 1024
    area = load(fn, size)
    for cnt in range(1024, np.max(area)):
        dist = find_path(area, cnt)
        print(cnt, dist)
        if not dist:
            print(np.where(area==cnt))
            return
