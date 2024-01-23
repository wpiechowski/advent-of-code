from dataclasses import dataclass

import numpy as np
import re


def load(fn):
    ret = []
    rx = re.compile(r"(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)")
    for line in open(fn):
        m = rx.match(line.strip())
        if m:
            v = tuple(map(int, m.group(1, 2, 3, 4, 5, 6)))
            ret.append(v)
            if v[0] > v[3] or v[1] > v[4] or v[2] > v[5]:
                print(v)
                raise ValueError("sort")
    ret.sort(key=lambda x: min(x[2], x[5]))
    return np.array(ret)


def get_extent(bricks: np.array):
    x_max = np.max(bricks[:, 0::3])
    y_max = np.max(bricks[:, 1::3])
    return y_max + 1, x_max + 1


def task1():
    fn = "i22a.txt"
    bricks = load(fn)
    # print(bricks)
    extent = get_extent(bricks)
    print(extent)
    heights = np.zeros(extent, int)
    z_buf = -np.ones(extent, int)
    fallen = np.zeros(bricks.shape, int)
    blocked = set()
    ret = set()
    for bn, b in enumerate(bricks):
        mask = np.zeros(extent, int)
        mask[b[1]: b[4] + 1, b[0]: b[3] + 1] = 1
        # print(b)
        # print(mask)
        y = np.max(heights[mask > 0])
        dy = y - b[2] + 1
        if y > 0:
            supp = set()
            under = np.argwhere((heights == y) & (mask > 0))
            for yy, xx in under:
                supp.add(z_buf[yy, xx])
            if len(supp) > 1:
                ret.update(supp)
            else:
                blocked.update(supp)
        fallen[bn, :] = b
        fallen[bn, 2::3] += dy
        heights[mask > 0] = fallen[bn, 5]
        z_buf[mask > 0] = bn
    cover = set(range(len(bricks))) - blocked - ret
    ret -= blocked
    print(len(ret | cover))


@dataclass
class Block:
    above: set[int]
    below: set[int]


def try_remove(links: dict[int, Block], bn: int):
    removed = {bn}
    q = []
    q.extend(links[bn].above)
    while q:
        bn = q.pop(0)
        if bn in removed:
            continue
        b = links[bn]
        if b.below - removed:
            continue
        q.extend(b.above)
        removed.add(bn)
    return len(removed) - 1


def task2():
    fn = "i22a.txt"
    bricks = load(fn)
    # print(bricks)
    extent = get_extent(bricks)
    heights = np.zeros(extent, int)
    z_buf = -np.ones(extent, int)
    fallen = np.zeros(bricks.shape, int)
    links = {}
    for bn in range(len(bricks)):
        links[bn] = Block(set(), set())
    for bn, b in enumerate(bricks):
        mask = np.zeros(extent, int)
        mask[b[1]: b[4] + 1, b[0]: b[3] + 1] = 1
        # print(b)
        # print(mask)
        y = np.max(heights[mask > 0])
        dy = y - b[2] + 1
        if y > 0:
            under_pos = np.argwhere((heights == y) & (mask > 0))
            for yy, xx in under_pos:
                under = z_buf[yy, xx]
                links[under].above.add(bn)
                links[bn].below.add(under)
        fallen[bn, :] = b
        fallen[bn, 2::3] += dy
        heights[mask > 0] = fallen[bn, 5]
        z_buf[mask > 0] = bn
    print(links)
    s = 0
    for bn in range(len(bricks)):
        x = try_remove(links, bn)
        s += x
        print(bn, x)
    print(s)
