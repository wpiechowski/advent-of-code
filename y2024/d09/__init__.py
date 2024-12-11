from collections import namedtuple
from itertools import chain

from tools import *


@dataclass
class Block:
    id: int
    size: int
    pos: int


def load_iter(fn: str):
    free = False
    num = 0
    pos = 0
    for line in get_lines(fn):
        for ch in line:
            i = int(ch)
            if free:
                yield Block(-1, i, pos)
            else:
                yield Block(num, i, pos)
                num += 1
            free = not free
            pos += i


def pr(files, gaps):
    size = 0
    for f in chain(files, gaps):
        size = max(size, f.pos + f.size)
    txt = "," * size
    for f in files:
        txt = txt[:f.pos] + str(f.id) * f.size + txt[f.pos + f.size:]
    for g in gaps:
        if g.size:
            txt = txt[:g.pos] + "." * g.size + txt[g.pos + g.size:]
    print(txt)


def task1():
    files = deque()
    gaps = deque()
    done = []
    for k in load_iter("i.txt"):
        if not k.size:
            continue
        if k.id < 0:
            gaps.append(k)
        else:
            files.append(k)
    if gaps[-1].pos < files[-1].pos:
        gaps.append(Block(-1, 0, files[-1].pos + files[-1].size))
    # pr(files, gaps)
    swaps = 0
    while True:
        g0 = gaps[0]
        f1 = files[-1]
        if g0.pos > f1.pos:
            break
        while files[0].pos < g0.pos:
            done.append(files.popleft())
        f1.size -= 1
        files.appendleft(Block(f1.id, 1, gaps[0].pos))
        gaps[-1].size += 1
        gaps[-1].pos -= 1
        gaps[0].size -= 1
        gaps[0].pos += 1
        while not gaps[0].size:
            gaps.popleft()
        if not f1.size:
            if len(gaps) >= 2 and gaps[-2].pos + gaps[-2].size == gaps[-1].pos:
                gaps[-2].size += gaps[-1].size
                gaps.pop()
            files.pop()
        swaps += 1
    done.extend(files)
    # pr(done, gaps)
    ret = 0
    for b in done:
        for i in range(b.size):
            ret += b.id * (b.pos + i)
    print(ret)


def task2():
    files = deque()
    gaps = deque()
    done = []
    for k in load_iter("i.txt"):
        if not k.size:
            continue
        if k.id < 0:
            gaps.append(k)
        else:
            files.append(k)
    if gaps[-1].pos < files[-1].pos:
        gaps.append(Block(-1, 0, files[-1].pos + files[-1].size))
    while files:
        f = files.pop()
        print(f.id)
        for g in gaps:
            if g.pos >= f.pos:
                break
            if g.size >= f.size:
                f.pos = g.pos
                g.pos += f.size
                g.size -= f.size
                break
        done.append(f)
    # pr(done, [Block(-1, 0, 0)])
    ret = 0
    for b in done:
        for i in range(b.size):
            ret += b.id * (b.pos + i)
    print(ret)
