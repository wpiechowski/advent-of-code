import time

from tools import *
import numpy as np
import pylab as plt


@dataclass
class Cart2:
    path: list[tuple[int, int, int]]
    pos: int
    turn: int


@dataclass
class Cart:
    pos: tuple[int, int]
    dir: tuple[int, int]
    turn: int

    def __lt__(self, other):
        return self.pos[0] < other.pos[0] or \
            (self.pos[0] == other.pos[0] and
             self.pos[1] < other.pos[1])


MAP_EMPTY = 0
MAP_GO_H = 1
MAP_GO_V = 2
MAP_CIACH = 3
MAP_UNCIACH = 4
MAP_CROSS = 5


def load(fn: str) -> tuple[np.array, list[Cart]]:
    dirs = {
        "v": (1, 0),
        "^": (-1, 0),
        "<": (0, -1),
        ">": (0, 1),
    }
    lines = list(get_lines(fn, strip=False))
    size_x = max(map(len, lines))
    size_y = len(lines)
    board = np.zeros((size_y, size_x), int)

    # def get(y, x):
    #     return lines[y][x] if x < len(lines[y]) else " "

    carts = []
    for y, line in enumerate(lines):
        for x, ch in enumerate(line):
            val = MAP_EMPTY
            if ch in "v^<>":
                c = Cart((y, x), dirs[ch], -1)
                carts.append(c)
                val = MAP_GO_H if ch in "<>" else MAP_GO_V
            elif ch == "-":
                val = MAP_GO_H
            elif ch == "|":
                val = MAP_GO_V
            elif ch == "/":
                val = MAP_CIACH
            elif ch == "\\":
                val = MAP_UNCIACH
            elif ch == "+":
                val = MAP_CROSS
            board[y, x] = val
    return board, carts


def step(board: np.array, cart: Cart):
    y, x = cart.pos
    dy, dx = cart.dir
    y += dy
    x += dx
    code = board[y, x]
    if code == MAP_CIACH:
        dy, dx = -dx, -dy
    elif code == MAP_UNCIACH:
        dy, dx = dx, dy
    elif code == MAP_CROSS and cart.turn == -1:
        dy, dx = -dx, dy
        cart.turn += 1
    elif code == MAP_CROSS and cart.turn == 1:
        dy, dx = dx, -dy
        cart.turn += 1
    elif code == MAP_CROSS and cart.turn == 0:
        cart.turn += 1
    elif code == MAP_EMPTY:
        raise ValueError("fall")
    cart.pos = y, x
    cart.dir = dy, dx
    if cart.turn == 2:
        cart.turn = -1


def plot(axes, board: np.array, carts: list[Cart]):
    d = np.zeros((board.shape[0] * 3, board.shape[1] * 3), int)
    images = {
        MAP_EMPTY: [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
        MAP_GO_H: [[0, 0, 0], [1, 1, 1], [0, 0, 0]],
        MAP_GO_V: [[0, 1, 0], [0, 1, 0], [0, 1, 0]],
        MAP_CROSS: [[0, 1, 0], [1, 1, 1], [0, 1, 0]],
        MAP_CIACH: [[0, 0, 1], [0, 1, 0], [1, 0, 0]],
        MAP_UNCIACH: [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
    }
    for y, x in product(range(board.shape[0]), range(board.shape[1])):
        d[y * 3: y * 3 + 3, x * 3: x * 3 + 3] = images[board[y, x]]
    for cart in carts:
        d[cart.pos[0] * 3: cart.pos[0] * 3 + 3, cart.pos[1] * 3: cart.pos[1] * 3 + 3] *= 2
    axes.imshow(d)


def task1():
    board, carts = load("i.txt")
    ic(carts)
    round = 0
    plt.ion()
    fig, ax = plt.subplots()
    while True:
        round += 1
        carts.sort()
        ax.clear()
        plot(ax, board, carts)
        plt.draw()
        fig.canvas.flush_events()
        pos = {c.pos for c in carts}
        for cart in carts:
            pos.remove(cart.pos)
            step(board, cart)
            if cart.pos in pos:
                ic(round, cart)
                time.sleep(10)
                return
            pos.add(cart.pos)
        # time.sleep(100)
        ic(round)


def task2():
    board, carts = load("i.txt")
    ic(carts)
    round = 0
    # plt.ion()
    # fig, ax = plt.subplots()
    while True:
        round += 1
        carts.sort()
        # ax.clear()
        # plot(ax, board, carts)
        # plt.draw()
        # fig.canvas.flush_events()
        pos = {c.pos for c in carts}
        dead = []
        for cart in carts:
            pos.remove(cart.pos)
            step(board, cart)
            if cart.pos in pos:
                for c in carts:
                    if c.pos == cart.pos:
                        dead.append(c)
            pos.add(cart.pos)
        for c in dead:
            if c in carts:
                carts.remove(c)
        if len(carts) < 2:
            break
        # time.sleep(100)
        ic(round, len(carts))
    ic(carts)



"""
dy dx	/	\	L	R
> 0 1	^ -1 0	v 1 0	^ -1 0	v 1 0
< 0 -1	v 1 0	^ -1 0	v 1 0	^ -1 0
v 1 0	< 0 -1	> 0 1	> 0 1	< 0 -1
^ -1 0	> 0 1	< 0 -1	< 0 -1	> 0 1
				
	-dx -dy	dx dy	-dx dy	dx -dy

"""