from tools import *
import numpy as np


def calc_hash(seed: str) -> bytes:
    count = 256
    data = list(range(count))
    offset = 0
    skip = 0
    vals = [ord(x) for x in seed]
    vals.extend([17, 31, 73, 47, 23])
    for _ in range(64):
        for val in vals:
            # print(skip, val, data)
            data[:val] = data[:val][::-1]
            pos = (val + skip) % count
            offset -= pos
            # print("   ", pos, data)
            if pos:
                data = data[pos:] + data[:pos]
            # print("   ", data)
            skip += 1
    offset %= count
    data = data[offset:] + data[:offset]
    blocks = []
    for b1 in range(0, count, 16):
        val = 0
        for b2 in range(16):
            val ^= data[b1 + b2]
        blocks.append(val)
    ret = bytes(blocks)
    return ret


def count_ones(data: bytes) -> int:
    ret = 0
    for b in data:
        b = int(b)
        for s in range(8):
            if b & (1 << s):
                ret += 1
    return ret


def task1():
    seed = "flqrgnkx"
    # seed = "hwlqcszp"
    r = 0
    for n in range(128):
        h = calc_hash(seed + "-" + str(n))
        r += count_ones(h)
    ic(r)


def find_one(data: np.array) -> tuple[int, int]:
    for y, line in enumerate(data):
        for x, v in enumerate(line):
            if v:
                return y, x


def clear_group(data: np.array, y: int, x: int):
    q = [(y, x)]
    while q:
        y, x = q.pop()
        if data[y, x] == 0:
            continue
        data[y, x] = 0
        for dx, dy, _ in directions:
            p = y + dy, x + dx
            if 0 <= p[0] < 128 and 0 <= p[1] < 128:
                if data[p]:
                    q.append(p)


def task2():
    # seed = "flqrgnkx"
    seed = "hwlqcszp"
    data = np.zeros((128, 128), int)
    for n in range(128):
        h = calc_hash(seed + "-" + str(n))
        for b in range(128):
            v = h[b // 8]
            if (v << (b & 7)) & 128:
                data[n, b] = 1
    ic(data)
    grps = 0
    while pos := find_one(data):
        grps += 1
        clear_group(data, *pos)
    ic(grps)
