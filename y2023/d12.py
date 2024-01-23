from functools import cache


def fit_here(points: str, block: int):
    if len(points) < block:
        return False
    for p in points[:block]:
        if p == ".":
            return False
    return True


def print_dec(func):
    def inner(points, blocks):
        ret = func(points, blocks)
        print(f"{points} {blocks} -> {ret}")
        return ret
    return inner


# 0 empty
# 1 unknown
# 2 full
# @print_dec
@cache
def count_possibles(points: str, blocks: tuple[int]) -> int:
    # print(f"check {points} {blocks}")
    if not points:
        return not blocks
    if points[0] == ".":
        return count_possibles(points[1:], blocks)
    if points[0] == "#":
        if not blocks:
            return 0
        if not fit_here(points, blocks[0]):
            return 0
        if len(points) == blocks[0]:
            return len(blocks) == 1
        if points[blocks[0]] == "#":
            return 0
        return count_possibles(points[blocks[0] + 1:], blocks[1:])
    # ?
    if not blocks:
        return count_possibles(points[1:], blocks)
    c = 0
    if fit_here(points, blocks[0]):
        if len(points) == blocks[0]:
            c += len(blocks) == 1
        elif points[blocks[0]] == "#":
            pass
        else:
            c += count_possibles(points[blocks[0] + 1:], blocks[1:])
    c += count_possibles(points[1:], blocks)
    return c


def load_line(line: str):
    points, b = line.split(" ")
    blocks = tuple(map(int, b.split(",")))
    return points, blocks


def task1():
    ret = 0
    for line in open("i12a.txt"):
        points, blocks = load_line(line.strip())
        c = count_possibles(points, blocks)
        print(points, blocks, c)
        ret +=c
    print(ret)


def task1b():
    points = "??"
    blocks = (2, 1)
    print(count_possibles(points, blocks))


def task2():
    ret = 0
    for line in open("i12a.txt"):
        points, blocks = load_line(line.strip())
        c = count_possibles("?".join([points] * 5), blocks * 5)
        print(points, blocks, c)
        ret +=c
    print(ret)
