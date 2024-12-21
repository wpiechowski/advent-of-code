from tools import *


layout_numpad = ["789", "456", "123", " 0A"]
layout_cursor = [" ^A", "<v>"]


A_NOP = (0, 0, "")
A_UP = (-1, 0, "")
A_RIGHT = (0, 1, "")
A_DOWN = (1, 0, "")
A_LEFT = (0, -1, "")
A_ACTION = (0, 0, "A")


actions = {
    "": A_NOP,
    "^": A_UP,
    ">": A_RIGHT,
    "v": A_DOWN,
    "<": A_LEFT,
    "A": A_ACTION,
}


class Keypad:
    def __init__(self, layout: list[str]):
        self.layout = layout
        self.pos: dict[str, tuple[int, int]] = {}
        self.init_pos(layout)
        self.hand = (0, 0)
        self.moves: dict[str: str] = {}
        self.calc_moves()
        self.set_state("A")

    def init_pos(self, layout: list[str]):
        for y, line in enumerate(layout):
            for x, ch in enumerate(line):
                if ch == " ":
                    continue
                self.pos[ch] = y, x

    def set_state(self, ch: str):
        self.hand = self.pos[ch]

    def get_state(self):
        return self.key_at(self.hand)

    def key_at(self, pos: tuple[int, int]):
        if not 0 <= pos[0] < len(self.layout):
            return " "
        if not 0 <= pos[1] < len(self.layout[0]):
            return " "
        return self.layout[pos[0]][pos[1]]

    def print(self):
        sel = self.get_state()
        for line in self.layout:
            txt = ""
            for ch in line:
                if ch == sel:
                    txt += f"[{ch}]"
                else:
                    txt += f" {ch} "
            print(txt)

    def action(self, action: tuple) -> tuple:
        self.hand = self.hand[0] + action[0], self.hand[1] + action[1]
        if self.get_state() == " ":
            raise ValueError("bad")
        if action[2] == "A":
            code = self.get_state()
            if code in "0123456789A":
                return 0, 0, code
            elif code == "^":
                return A_UP
            elif code == ">":
                return A_RIGHT
            elif code == "v":
                return A_DOWN
            elif code == "<":
                return A_LEFT
        return A_NOP

    def play(self, moves: str):
        for m in moves:
            self.action(actions[m])

    def calc_move(self, a: str, b: str) -> str:
        if a == b:
            return ""
        pa = self.pos[a]
        pb = self.pos[b]
        dy = pb[0] - pa[0]
        dx = pb[1] - pa[1]
        ty = ("v" * dy) + ("^" * -dy)
        tx = (">" * dx) + ("<" * -dx)
        if dx > 0:
            t1 = ty + tx
            t2 = tx + ty
        else:
            t1 = tx + ty
            t2 = ty + tx
        try:
            self.set_state(a)
            self.play(t1)
            return t1
        except ValueError:
            return t2

    def calc_moves(self):
        them = "".join(self.layout)
        for ch1 in them:
            if ch1 == " ":
                continue
            for ch2 in them:
                if ch2 == " ":
                    continue
                self.moves[ch1 + ch2] = self.calc_move(ch1, ch2)


def get_state(pads: list[Keypad]) -> str:
    return pads[0].get_state() + pads[1].get_state() + pads[2].get_state()


def set_state(pads: list[Keypad], s: str):
    pads[0].set_state(s[0])
    pads[1].set_state(s[1])
    pads[2].set_state(s[2])


def find_moves(request: str, pad: Keypad) -> str:
    ret = ""
    state = "A"
    for ch in request:
        ret += pad.moves[state + ch] + "A"
        state = ch
    return ret


def replay(pads: list[Keypad], moves: str) -> str:
    set_state(pads, "AAA")
    ret = ""
    for m in moves:
        a = actions[m]
        for p in pads:
            a = p.action(a)
        ret += a[2]
    return ret


def task1():
    pads = [Keypad(layout_cursor), Keypad(layout_cursor), Keypad(layout_numpad)]
    score = 0
    for moves in get_lines("i.txt"):
        m0 = moves
        print(moves)
        for pad in reversed(pads):
            moves = find_moves(moves, pad)
            print(moves)
        score += len(moves) * int(m0[:-1])
        r = replay(pads, moves)
        print(m0, r)
    print(score)


@cache
def count_moves(pad: Keypad, moves: str, iters: 25) -> int:
    if iters == 0:
        return len(moves)
    count = 0
    state = "A"
    for m in moves:
        mm = pad.moves[state + m] + "A"
        state = m
        count += count_moves(pad, mm, iters - 1)
    return count


def task2():
    numpad = Keypad(layout_numpad)
    cursor = Keypad(layout_cursor)
    score = 0
    for moves in get_lines("i.txt"):
        m0 = moves
        print(moves)
        moves = find_moves(moves, numpad)
        cnt = count_moves(cursor, moves, 25)
        print(cnt)
        score += cnt * int(m0[:-1])
    print(score)
