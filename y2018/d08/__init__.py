from tools import *


@dataclass
class Node:
    subs: list
    meta: list[int]

    def load(self, data: list[int], pos: int = 0) -> int:
        sub_cnt = data[pos]
        meta_cnt = data[pos + 1]
        self.subs = []
        pos += 2
        for _ in range(sub_cnt):
            sub = Node([], [])
            pos = sub.load(data, pos)
            self.subs.append(sub)
        self.meta = data[pos: pos + meta_cnt]
        pos += meta_cnt
        return pos

    def get_sum(self) -> int:
        s = sum([x.get_sum() for x in self.subs])
        s += sum(self.meta)
        return s

    def get_value(self) -> int:
        if not self.subs:
            return sum(self.meta)
        vals = [-1] * len(self.subs)
        ret = 0
        for m in self.meta:
            m -= 1
            if m < 0 or m >= len(self.subs):
                continue
            if vals[m] == -1:
                vals[m] = self.subs[m].get_value()
            ret += vals[m]
        return ret


def task1():
    for line in get_int_lines("i.txt"):
        root = Node([], [])
        root.load(line)
        ic(root.get_sum())


def task2():
    for line in get_int_lines("i.txt"):
        root = Node([], [])
        root.load(line)
        ic(root.get_value())
