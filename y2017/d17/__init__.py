from tools import *


def spinlock(step: int, count: int):
    buf = [0]
    pos = 0
    t = time.time()
    for k in range(count):
        pos = (pos + step) % len(buf)
        if pos < len(buf) - 1:
            pos += 1
            buf = buf[:pos] + [k + 1] + buf[pos:]
        else:
            pos = len(buf)
            buf.append(k + 1)
        now = time.time()
        if now - t > 1:
            t = now
            ic(k, pos)
    p = buf.index(0)
    ic(buf[p + 1])


def spinlock2(step: int, count: int):
    pos = 0
    pos1 = 0
    size = 1
    for k in range(count):
        pos = (pos + step) % size
        if pos < size - 1:
            pos += 1
        else:
            pos = size
        size += 1
        if pos == 1:
            pos1 = k + 1
        # ic(k, pos1)
    ic(pos1)


def task1():
    # spinlock2(3, 10)
    spinlock2(324, 50000000)
