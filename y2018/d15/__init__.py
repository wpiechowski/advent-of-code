from tools import *
import numpy as np
import pylab as plt


MAP_EMPTY = 0
MAP_G = 512
MAP_E = 256
MAP_WALL = 256 + 512


def load(fn: str):
    lines = []
    hp = 200
    for line in get_lines(fn):
        vals = []
        for ch in line:
            if ch == ".":
                val = MAP_EMPTY
            elif ch == "#":
                val = MAP_WALL
            elif ch == "G":
                val = MAP_G + hp
            elif ch == "E":
                val = MAP_E + hp
            else:
                raise ValueError(ch)
            vals.append(val)
        lines.append(vals)
    return np.array(lines)


def print_map(data: np.array):
    for line in data:
        txt = ""
        for val in line:
            if val == MAP_EMPTY:
                ch = "."
            elif val == MAP_WALL:
                ch = "#"
            elif val & 0xff00 == MAP_G:
                ch = "G"
            elif val & 0xff00 == MAP_E:
                ch = "E"
            txt += ch
        print(txt)


def get_in_range(data: np.array, pos: tuple[int, int]):
    expect = get_expected(data[pos])
    y, x = pos
    ret = []
    for dy, dx, _ in directions:
        py, px = y + dy, x + dx
        if data[py, px] & 0xff00 == expect:
            ret.append((data[py, px] & 0xff, py, px))
    return ret


def dist_map(data: np.array, pos: tuple[int, int]):
    q = deque([(0, pos[0], pos[1])])
    expect = get_expected(data[pos])
    found = []  # dist, y, x
    while q:
        dist, y, x = q.popleft()
        if dist > 250:
            raise ValueError("distance too big")
        if found and dist >= found[0][0]:
            break
        dist += 1
        for dy, dx, _ in directions:
            py, px = y + dy, x + dx
            d = data[py, px]
            if d & 0xff00 == expect:
                found.append((dist, py, px))
            elif d == MAP_EMPTY:
                data[py, px] = dist
                q.append((dist, py, px))
    return found


def get_expected(data_pos):
    color = data_pos & 0xff00
    if color == MAP_G:
        expect = MAP_E
    else:
        expect = MAP_G
    return expect


def collect_paths(data: np.array, pos: tuple[int, int], found: list[tuple[int, ...]]):
    q = deque(found)
    ret = []
    while q:
        dist, y, x = q.popleft()
        if data[y, x] < 0:
            continue
        data[y, x] *= -1
        if data[y, x] == -1:
            ret.append((y, x))
        for dy, dx, _ in directions:
            py, px = y + dy, x + dx
            if data[py, px] == dist - 1:
                q.append((dist - 1, py, px))
    data[data <= -0x100] *= -1
    return ret


def get_players(data: np.array) -> tuple[dict[tuple[int, int], int], bool]:
    ret = {}
    gs = 0
    es = 0
    for y, line in enumerate(data):
        for x, val in enumerate(line):
            if val & 0xff00 == MAP_G:
                gs += 1
            elif val & 0xff00 == MAP_E:
                es += 1
            if val & 0xff00 in (MAP_G, MAP_E):
                ret[(y, x)] = val
    return ret, not (gs * es)


def move(data: np.array, e_attack):
    players, done = get_players(data)
    if done:
        return False
    killed = set()
    # ic(players)
    for pos, ge_hp in players.items():
        if pos in killed:
            continue
        data[data < 0x100] = 0
        in_range = get_in_range(data, pos)
        if not in_range:
            found = dist_map(data, pos)
            if not found:
                continue
            paths = collect_paths(data, pos, found)
            if not paths:
                continue
            new_pos = min(paths)
            data[new_pos] = data[pos]
            data[pos] = 0
            pos = new_pos
            in_range = get_in_range(data, pos)
        if in_range:
            hp, ty, tx = min(in_range)
            target = ty, tx
            if data[pos] & 0xff00 == MAP_E:
                attack = e_attack
            else:
                attack = 3
            if hp > attack:
                data[target] -= attack
            else:
                killed.add(target)
                data[target] = 0
    _, done = get_players(data)
    return not done


def plot(ax, data: np.array):
    img = np.zeros((data.shape[0], data.shape[1], 3), int)
    img[data == MAP_WALL, :] = [128, 128, 120]
    fg = data & 0xff00 == MAP_G
    img[fg, 0] = data[fg] & 0xff
    img[fg, 1] = 128
    img[fg, 2] = 0
    fg = data & 0xff00 == MAP_E
    img[fg, 0] = data[fg] & 0xff
    img[fg, 1] = 0
    img[fg, 2] = 128
    ax.imshow(img)


def task1():
    data = load("i.txt")
    plt.ion()
    fig, ax = plt.subplots()
    round = 0
    while move(data, 3):
        round += 1
        ic(round)
        plot(ax, data)
        ax.set_title(str(round))
        plt.draw()
        fig.canvas.flush_events()
    players, _ = get_players(data)
    for pos, v in players.items():
        ic(pos, v & 0xff)
    s = sum(v & 0xff for v in players.values())
    # round -= 1
    ic(s, round, s * round)
    plt.ioff()
    plt.show()


def count_e(data: np.array):
    ret = 0
    for line in data:
        for val in line:
            if val & 0xff00 == MAP_E:
                ret += 1
    return ret


def task2():
    data = load("i.txt")
    plt.ion()
    fig, ax = plt.subplots()
    round = 0
    e0 = count_e(data)
    while move(data, 34):
        round += 1
        ic(round)
        plot(ax, data)
        ax.set_title(str(round))
        plt.draw()
        fig.canvas.flush_events()
    e1 = count_e(data)
    ic(e0, e1)
    players, _ = get_players(data)
    for pos, v in players.items():
        ic(pos, v & 0xff)
    s = sum(v & 0xff for v in players.values())
    # round -= 1
    ic(s, round, s * round)
    plt.ioff()
    plt.show()
