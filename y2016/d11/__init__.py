import re
import time
from collections import deque

from tools import get_lines

fn = "i2.txt"


def load():
    floors = []
    words = {}
    re_chip = re.compile(r"(\w+)-compatible")
    re_gen = re.compile(r"(\w+) generator")
    for floor, line in enumerate(get_lines(fn)):
        s = set()
        # ic(line)
        for gen in re_gen.finditer(line):
            name = gen[1]
            if name not in words:
                words[name] = len(words) + 1
            s.add(words[name])
        for chip in re_chip.finditer(line):
            name = chip[1]
            if name not in words:
                words[name] = len(words) + 1
            s.add(-words[name])
        # ic(s)
        floors.append(frozenset(s))
    return (0, tuple(floors)), len(words)


def is_valid_floor(floor: frozenset[int]) -> bool:
    gens = {g for g in floor if g > 0}
    if not gens:
        return True
    chips = floor - gens
    for chip in chips:
        if -chip not in floor:
            return False
    return True


def evolve(state: tuple[int, tuple[frozenset[int], ...]]):
    elev, floors = state
    floor = list(floors[elev])
    for n_item1, item1 in enumerate(floor):
        for item2 in floor[:n_item1 + 1]:
            if item2 == item1:
                bag = frozenset({item1})
            else:
                bag = frozenset({item1, item2})
            if not is_valid_floor(bag):
                continue
            if not is_valid_floor(floors[elev] - bag):
                continue
            ee = []
            if elev > 0:
                ee.append(elev - 1)
            if elev < len(floors) - 1:
                ee.append(elev + 1)
            for next_elev in ee:
                if not is_valid_floor(floors[next_elev] | bag):
                    continue
                f2 = list(floors)
                f2[elev] = f2[elev] - bag
                f2[next_elev] = f2[next_elev] | bag
                yield next_elev, tuple(f2)
            if not item2:
                break



def task1():
    target, item_count = load()
    ic(target, item_count)
    state = 3, (frozenset(), frozenset(), frozenset(), frozenset(range(1, item_count + 1)) | set(range(-item_count, 0)))
    ic(state)
    q = deque([(state, 0)])
    cache = {state: 0}
    pt = time.time()
    while q:
        state, moves = q.popleft()
        now = time.time()
        if now - pt > 1:
            ic(len(q), moves)
            pt = now
        if state == target:
            ic(moves)
            return
        for s2 in evolve(state):
            if s2 in cache:
                continue
            cache[s2] = moves + 1
            q.append((s2, moves + 1))
