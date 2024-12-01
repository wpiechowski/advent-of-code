from tools import *
from dataclasses import dataclass


@dataclass
class Layer:
    depth: int
    range: int

    def pos_at(self, t: int) -> int:
        t %= self.range * 2 - 2
        if t >= self.range:
            t -= self.range
            t = self.range - t - 2
        return t


def load() -> list[Layer]:
    fn = "i.txt"
    rx = r"(\d+): (\d+)"
    ret = []
    for depth, range in get_re_lines(fn, rx):
        ret.append(Layer(int(depth), int(range)))
    return ret


def task1():
    layers = load()
    score = 0
    for l in layers:
        if l.pos_at(l.depth) == 0:
            score += l.depth * l.range
    ic(score)


def task2():
    layers = load()
    for t in range(10000000):
        for l in layers:
            if l.pos_at(l.depth + t) == 0:
                break
        else:
            break
    ic(t)
