from tools import get_lines, get_path

fn = "i.txt"


cache = set()
cache_hits = 0
shortest = 0


def equal_groups(vals: tuple[int, ...], weights: tuple[int, ...], counts: tuple[int, ...]):
    if not vals:
        if weights[0] == weights[1] and weights[0] == weights[2]:
            yield [], [], []
        return
    h = max(weights)
    s = 3 * h - sum(weights)
    if s > sum(vals):
        return
    if min(counts) > shortest:
        return
    global cache, cache_hits
    key = vals, weights
    if key in cache:
        cache_hits += 1
        # return
    v0 = vals[0]
    vt = vals[1:]
    for g in range(3):
        z = list(weights)
        z[g] += v0
        c = list(counts)
        c[g] += 1
        for res in equal_groups(vt, tuple(z), tuple(c)):
            res[g].append(v0)
            cache.add(key)
            yield res


def calc_entang(vals: list[int]) -> int:
    r = 1
    for v in vals:
        r *= v
    return r


def task1():
    vals = [int(x) for x in get_lines(get_path() + fn)]
    vals.reverse()
    worst = calc_entang(vals)
    vals = tuple(vals)
    global shortest
    shortest = len(vals)
    best_ent = worst
    for c in equal_groups(vals[1:],(vals[0], 0, 0), (1, 0, 0)):
        c[0].append(vals[0])
        l = min(map(len, c))
        if l > shortest:
            continue
        if l < shortest:
            best_ent = worst
        shortest = min(l, shortest)
        e = list(map(calc_entang, c))
        b = worst
        for g1 in range(3):
            if len(c[g1]) == l:
                b = min(b, e[g1])
        best_ent = min(best_ent, b)
        print(shortest, best_ent, c)


def equal_groups2(vals: tuple[int, ...], weights: tuple[int, ...], counts: tuple[int, ...]):
    if not vals:
        if weights[0] == weights[1] and weights[0] == weights[2] and weights[0] == weights[3]:
            yield [], [], [], []
        return
    h = max(weights)
    s = 4 * h - sum(weights)
    if s > sum(vals):
        return
    if min(counts) > shortest:
        return
    global cache, cache_hits
    key = vals, weights
    if key in cache:
        cache_hits += 1
        # return
    v0 = vals[0]
    vt = vals[1:]
    used = sum(counts)
    for g in range(min(4, used + 1)):
        z = list(weights)
        z[g] += v0
        c = list(counts)
        c[g] += 1
        for res in equal_groups2(vt, tuple(z), tuple(c)):
            res[g].append(v0)
            cache.add(key)
            yield res


def task2():
    vals = [int(x) for x in get_lines(get_path() + fn)]
    vals.reverse()
    worst = calc_entang(vals)
    vals = tuple(vals)
    global shortest
    shortest = len(vals)
    best_ent = worst
    for c in equal_groups2(vals,(0, 0, 0, 0), (0, 0, 0, 0)):
        l = min(map(len, c))
        if l > shortest:
            continue
        if l < shortest:
            best_ent = worst
        shortest = min(l, shortest)
        e = list(map(calc_entang, c))
        b = worst
        for g1 in range(4):
            if len(c[g1]) == l:
                b = min(b, e[g1])
        best_ent = min(best_ent, b)
        print(shortest, best_ent, c)


# 74850409
# 83754553