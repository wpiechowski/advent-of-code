from tools import *


def load() -> tuple[tuple[int, int]]:
    fn = "i.txt"
    ret = []
    for a, b in get_int_lines(fn):
        a, b = min_max((a, b))
        ret.append((a, b))
    return tuple(ret)


cache: dict[tuple[int, int], tuple[int, list[int]]] = {}


def find_best(items: tuple[tuple[int, int]], taken: int, needed: int) -> tuple[int, list[int]]:
    global cache
    key = taken, needed
    if key in cache:
        return cache[key]
    best_val = 0
    best_path = []
    for i, item in enumerate(items):
        if taken & (1 << i):
            continue
        if needed not in item:
            continue
        n = item[0] if needed == item[1] else item[1]
        b, p = find_best(items, taken | (1 << i), n)
        b += item[0] + item[1]
        if len(p) + 1 > len(best_path) \
                or (len(p) + 1 == len(best_path) and b > best_val):
            best_val = b
            best_path = [item] + p
    # cache[key] = best_val, best_path
    return best_val, best_path


def task1():
    items = load()
    taken = 0
    r = find_best(items, taken, 0)
    ic(r)
