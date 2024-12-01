from itertools import repeat

from tools import *


# count, fn = 5, "s.txt"
count, fn = 256, "i.txt"


def task1():
    data = list(range(count))
    offset = 0
    skip = 0
    for line in get_int_lines(fn):
        for val in line:
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
    print(data[offset] * data[(offset + 1) % count])


def task2():
    data = list(range(count))
    offset = 0
    skip = 0
    vals = []
    for line in get_lines(fn):
        vals = [ord(x) for x in line]
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
    hash = bytes(blocks).hex()
    print(hash)
