import re
import math


def process(time: int, dist: int) -> int:
    # (time - p) * p > dist
    # -p**2 + p*time - dist > 0
    d = math.sqrt(time**2 - 4 * dist)
    p1 = (-time - d) / -2
    p2 = (-time + d) / -2
    p1, p2 = min(p1, p2), max(p1, p2)
    if p1 == math.ceil(p1):
        p1 = int(p1 + 1)
    else:
        p1 = math.ceil(p1)
    if p2 == math.floor(p2):
        p2 = int(p2 - 1)
    else:
        p2 = math.floor(p2)
    print(p1, p2)
    return p2 - p1 + 1


def task1():
    f = open("i06a.txt")
    time_line = next(f)
    times = re.split(r"[ ]+", time_line[5:].strip())
    times = map(int, times)
    dist_line = next(f)
    dists = re.split(r"[ ]+", dist_line[9:].strip())
    dists = map(int, dists)
    ret = 1
    for time, dist in zip(times, dists):
        ret *= process(time, dist)
    print(ret)


def task2():
    ret = process(40817772, 219101213651089)
    print(ret)
