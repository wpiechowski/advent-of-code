import time


class Elf:
    def __init__(self, num: int, left: int, right: int):
        self.num = num
        self.left = left
        self.right = right
        self.count = 1

    def __repr__(self):
        return f"Elf({self.num}, {self.left}, {self.right}, {self.count})"


def init(count: int) -> list[Elf]:
    ret = []
    for n in range(count):
        e = Elf(n, (n + 1) % count, (n - 1) % count)
        ret.append(e)
    return ret


def turn(party: list[Elf], current: int) -> int:
    e = party[current]
    left = party[e.left]
    e.count += left.count
    left.count = 0
    e.left = left.left
    party[left.left].right = e.num
    return e.left


def task1():
    cnt = 3017957
    party = init(cnt)
    print("start")
    prev = 0
    current = 0
    while party[prev].count < cnt:
        prev = current
        current = turn(party, current)
        print(prev, party[prev].count)
    print(prev)


def task2():
    cnt = 3017957
    data = list(range(1, cnt + 1))
    cur_pos = 0
    t = time.time()
    while len(data) > 1:
        victim = cur_pos + len(data) // 2
        if victim >= len(data):
            victim -= len(data)
        else:
            cur_pos += 1
        now = time.time()
        if now - t > 1:
            t = now
            ic(len(data), cur_pos, victim)
        data.pop(victim)
        if cur_pos >= len(data):
            cur_pos = 0
    print(data)
