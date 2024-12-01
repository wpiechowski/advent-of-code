from collections import deque

# seed = 10
# target = 4, 7

seed = 1358
target = 39, 31


def is_wall(y: int, x: int) -> bool:
    p = x*x + 3*x + 2*x*y + y + y*y
    p += seed
    bits = 0
    while p:
        if p & 1:
            bits += 1
        p >>= 1
    return bits & 1 > 0


def task1():
    for y in range(10):
        txt = ""
        for x in range(10):
            txt += "#" if is_wall(y, x) else "."
        print(txt)
    pos = 1, 1
    visited = set()
    q = deque([(pos, 0, (pos,))])
    while q:
        (y, x), dist, hist = q.popleft()
        if (y, x) in visited:
            continue
        if (y, x) == target:
            ic(dist)
            return
        visited.add((y, x))
        for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            py, px = y + dy, x + dx
            if px < 0 or py < 0:
                continue
            if is_wall(py, px):
                continue
            q.append(((py, px), dist + 1, hist + ((py, px),)))


def task2():
    for y in range(10):
        txt = ""
        for x in range(10):
            txt += "#" if is_wall(y, x) else "."
        print(txt)
    pos = 1, 1
    visited = set()
    q = deque([(pos, 0)])
    while q:
        (y, x), dist = q.popleft()
        if (y, x) in visited:
            continue
        if dist > 50:
            ic(len(visited))
            return
        visited.add((y, x))
        for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            py, px = y + dy, x + dx
            if px < 0 or py < 0:
                continue
            if is_wall(py, px):
                continue
            q.append(((py, px), dist + 1))
