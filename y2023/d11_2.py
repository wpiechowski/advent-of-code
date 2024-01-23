def busy_to_gaps(vals: set[int]):
    # vals = list(vals)
    # vals.sort()
    ret = []
    for n in range(max(vals)):
        if n not in vals:
            ret.append(n)
    return ret


def load_map(fn: str):
    stars = []
    busy_x = set()
    busy_y = set()
    for y, line in enumerate(open(fn)):
        for x, ch in enumerate(line):
            if ch == "#":
                stars.append((x, y))
                busy_x.add(x)
                busy_y.add(y)
    return stars, busy_to_gaps(busy_x), busy_to_gaps(busy_y)


def gaps_between(x1: int, x2: int, gaps: list[int]):
    ret = 0
    x1, x2 = min(x1, x2), max(x1, x2)
    for g in gaps:
        if x1 < g < x2:
            ret += 1
    return ret


def calc_dist(s1, s2, gaps_x, gaps_y):
    w = 1000000
    gx = (w - 1) * gaps_between(s1[0], s2[0], gaps_x)
    gy = (w - 1) * gaps_between(s1[1], s2[1], gaps_y)
    # print(s1, s2, gx, gy)
    return abs(s1[0] - s2[0]) + abs(s1[1] - s2[1]) + gx + gy


def task2():
    stars, gaps_x, gaps_y = load_map("i11a.txt")
    print(stars)
    print(gaps_x, gaps_y)
    ret = 0
    for s1 in stars:
        for s2 in stars:
            if s1 == s2:
                break
            ret += calc_dist(s1, s2, gaps_x, gaps_y)
    print(ret)
