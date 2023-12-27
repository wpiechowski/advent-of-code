import numpy as np
import pylab as plt
import heapq
import time


def load(fn: str) -> tuple[np.array, int, int]:
    sx = 0
    sy = 0
    arr = []
    for y, line in enumerate(open(fn)):
        arr.append([])
        for x, ch in enumerate(line.strip()):
            if ch == "#":
                arr[-1].append(1)
            else:
                arr[-1].append(0)
            if ch == "S":
                sy, sx = y, x
    return np.array(arr), sy, sx


def plot(maze: np.array, cur: set[tuple[int, int]]):
    empty = 0
    for y, line in enumerate(maze):
        text = ""
        for x, ch in enumerate(line):
            if (y, x) in cur:
                text += "O"
            elif maze[y, x]:
                text += "#"
            else:
                text += "."
                empty += 1
        print(text)
    print(f"{empty=}")


def task1():
    fn = "i21a.txt"
    maze, y, x = load(fn)
    # print(maze)
    cur = {(y, x)}
    for _ in range(64):
        c2 = set()
        for y, x in cur:
            for dy, dx in ((0, 1), (1, 0), (-1, 0), (0, -1)):
                px = x + dx
                py = y + dy
                if px < 0 or px >= maze.shape[1]:
                    continue
                if py < 0 or py >= maze.shape[0]:
                    continue
                if maze[py, px]:
                    continue
                c2.add((py, px))
        cur = c2
        # plot(maze, cur)
    print(len(cur), cur)


def do_step(maze: np.array, cur: np.array) -> np.array:
    ret = np.zeros(cur.shape, dtype=int)
    ret[:-1, :] |= (~maze[:-1, :]) & cur[1:, :]
    ret[1:, :] |= (~maze[1:, :]) & cur[:-1, :]
    ret[:, :-1] |= (~maze[:, :-1]) & cur[:, 1:]
    ret[:, 1:] |= (~maze[:, 1:]) & cur[:, :-1]
    return ret


ee_cache = {}


def entry_exits(maze: np.array, y: int, x: int):
    global ee_cache
    if (y, x) in ee_cache:
        return ee_cache[y, x]
    exits = []
    for _ in range(4):
        exits.append((-1, -1, -1))
    cur = np.zeros(maze.shape, int)
    cur[y, x] = 1
    if maze.shape == (11, 11):
        max_sum = 42
    elif maze.shape == (131, 131):
        max_sum = 7424
    else:
        raise ValueError("max_sum unknown")
    for step in range(1, 200):
        cur = do_step(maze, cur)
        # N
        if exits[0][0] < 0:
            if np.any(cur[0, :]):
                exits[0] = (0, np.argmax(cur[0, :]), step)
        # E
        if exits[1][0] < 0:
            if np.any(cur[:, -1]):
                exits[1] = (np.argmax(cur[:, -1]), cur.shape[1] - 1, step)
        # S
        if exits[2][0] < 0:
            if np.any(cur[-1, :]):
                exits[2] = (cur.shape[0] - 1, np.argmax(cur[-1, :]), step)
        # W
        if exits[3][0] < 0:
            if np.any(cur[:, 0]):
                exits[3] = (np.argmax(cur[:, 0]), 0, step)
        if np.sum(cur) == max_sum:
            break
    ee_cache[y, x] = step, exits
    return step, exits


def find_full():
    fn = "i21s.txt"
    maze, y, x = load(fn)
    counts = []
    cur = np.zeros(maze.shape, int)
    cur[y, x] = 1
    for step in range(1, 1000):
        cur = do_step(maze, cur)
        s = np.sum(cur)
        print(step, s)
        counts.append(s)
    plt.plot(counts)
    plt.show()
    # duzy:
    # 140 7424
    # 141 7388
    # maly:
    # 990 42
    # 991 39


class Block:
    def __init__(self, maze: np.array, y: int, x: int, step0: int, by: int, bx: int):
        self.maze = maze
        self.y0 = y
        self.x0 = x
        self.step0 = step0
        self.by = by
        self.bx = bx
        step_full, self.exits = entry_exits(maze, y, x)
        self.step_full = self.step0 + step_full

    def events(self):
        ret = []    # (by, bx, y0, x0, step0)
        ex = self.exits
        ms = self.maze.shape
        if self.y0 > 0:
            ret.append((ex[0][2] + 1 + self.step0, self.by - 1, self.bx, ms[0] - 1, ex[0][1]))
        if self.x0 < ms[1] - 1:
            ret.append((ex[1][2] + 1 + self.step0, self.by, self.bx + 1, ex[1][0], 0))
        if self.y0 < ms[0] - 1:
            ret.append((ex[2][2] + 1 + self.step0, self.by + 1, self.bx, 0, ex[2][1]))
        if self.x0 > 0:
            ret.append((ex[3][2] + 1 + self.step0, self.by, self.bx - 1, ex[3][0], ms[1] - 1))
        ret.append((self.step_full, self.by, self.bx, -1, -1))
        return ret


def task2p():
    fn = "i21a.txt"
    maze, y, x = load(fn)
    steps, exits = entry_exits(maze, y, x)
    b = Block(maze, y, x, 0, 0, 0)
    blocks = {
        (0, 0): b,
    }
    max_step = 1000
    full_even = 0
    full_odd = 0
    completed = set()
    events = b.events()
    heapq.heapify(events)
    t0 = time.time()
    last_t = t0
    last_steps = 0
    while events:
        event = heapq.heappop(events)
        # print(event)
        if event[0] >= max_step:
            break
        step, by, bx, y0, x0 = event
        now = time.time()
        if now > last_t + 1:
            last_t = now
            print(step, step - last_steps, len(ee_cache))
            last_steps = step
        if y0 < 0:
            # full
            if step & 1:
                full_odd += 1
            else:
                full_even += 1
            del blocks[by, bx]
            completed.add((by, bx))
        if (by, bx) not in blocks and (by, bx) not in completed:
            b = Block(maze, y0, x0, step, by, bx)
            blocks[by, bx] = b
            for e in b.events():
                heapq.heappush(events, e)
        # else:
        #     print(f"{by},{bx} exists")
    print(f"{len(blocks)=}, {len(completed)=}, {full_odd=}, {full_even=}, {step=}")
    print(f"{maze.shape=}")
    for k, v in ee_cache.items():
        print(k, v)


def task2x():
    fn = "i21a.txt"
    maze, y, x = load(fn)
    # steps, exits = entry_exits(maze, y, x)
    # 26501365 = 65 + 131 * 202300
    mul = 6
    steps = 65 + mul * 131
    maze2 = np.hstack((maze,) * (mul * 2 + 1))
    maze2 = np.vstack((maze2,) * (mul * 2 + 1))
    x += mul * 131
    y += mul * 131
    cur = np.zeros(maze2.shape, int)
    cur[y, x] = 1
    for step in range(steps):
        print(f"{step}/{steps}")
        cur = do_step(maze2, cur)
    print("sum", np.sum(cur))
    mask = np.zeros(maze.shape, int)
    for y in range(132 // 2):
        mask[y, 65-y:66+y] = 1
        mask[130-y, 65-y:66+y] = 1
    # for y in range(maze2.shape[0]):
    #     for x in range(maze2.shape[1]):
    #         k1 = ((x + y - 65) // 131) % 2
    #         k2 = ((x - y - 65) // 131) % 2
    #         if k1 == 1 and k2 % 2 == 1:
    #             cur[y, x] = 1
    x0 = mul*131 + 131 - 65
    y0 = mul*131 + 131 - 65
    sub = cur[y0:y0+131, x0:x0+131] & mask
    print("sub", np.sum(sub))
    cur[y0:y0+131, x0:x0+131] = mask
    fig, ax = plt.subplots()
    # cur[:131, :131] = mask
    ax.imshow(maze2 * 0 + cur)
    plt.tight_layout()
    plt.show()


def task2():
    # 2: 92857
    # 4: 300451
    # 6: 626541
    m = 202300
    # m = 6
    a = 3759
    b = 3646
    c = 3639 - 1
    d = 3769
    m1 = m + 1
    r = a*m1*m1 + b*m*m + c*m*m1 + d*m*m1
    print(r)
