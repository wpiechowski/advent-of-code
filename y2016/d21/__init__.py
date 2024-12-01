from tools import min_max, get_lines
import re


fn = "i.txt"


def oper_swap_pos(x: str, pos1: str, pos2: str) -> str:
    pos1 = int(pos1)
    pos2 = int(pos2)
    pos1, pos2 = min_max(pos1, pos2)
    x = x[:pos1] + x[pos2] + x[pos1 + 1: pos2] + x[pos1] + x[pos2 + 1:]
    return x


def oper_swap_chars(x: str, ch1: str, ch2: str) -> str:
    x = x.replace(ch1, "/").replace(ch2, ch1).replace("/", ch2)
    return x


def oper_rot(x: str, d: str, steps: str) -> str:
    steps = int(steps) % len(x)
    if d == "left":
        x = x[steps:] + x[:steps]
    else:
        x = x[-steps:] + x[:-steps]
    return x


def oper_rot_inv(x: str, d: str, steps: str) -> str:
    return oper_rot(x, "left" if d == "right" else "right", steps)


def oper_rot_pos(x: str, ch: str) -> str:
    n = x.index(ch)
    return oper_rot(x, "right", n + 1 + (n >= 4))


def oper_rot_pos_inv(x: str, ch: str) -> str:
    n = x.index(ch)
    if n == 0:
        pos0 = 7
    elif n & 1:
        pos0 = (n - 1) // 2
    else:
        pos0 = n // 2 + 3
    ret = oper_rot(x, "left", n - pos0)
    return ret


def oper_reverse(x: str, p1: str, p2: str) -> str:
    p1 = int(p1)
    p2 = int(p2)
    p1, p2 = min_max(p1, p2)
    x = x[:p1] + x[p1: p2 + 1][::-1] + x[p2 + 1:]
    return x


def oper_move(x: str, p1: str, p2: str) -> str:
    p1 = int(p1)
    p2 = int(p2)
    ch = x[p1]
    x = x[:p1] + x[p1 + 1:]
    x = x[:p2] + ch + x[p2:]
    return x


def oper_move_inv(x: str, p1: str, p2: str) -> str:
    return oper_move(x, p2, p1)


cmds = [
    (re.compile(r"swap position (\d+) [a-z ]+ (\d+)"), oper_swap_pos, oper_swap_pos),
    (re.compile(r"swap letter (.) with letter (.)"), oper_swap_chars, oper_swap_chars),
    (re.compile(r"rotate (left|right) (\d+) \w+"), oper_rot, oper_rot_inv),
    (re.compile(r"rotate based [a-z ]+ letter (.)"), oper_rot_pos, oper_rot_pos_inv),
    (re.compile(r"reverse positions (\d+) through (\d+)"), oper_reverse, oper_reverse),
    (re.compile(r"move position (\d+) to position (\d+)"), oper_move, oper_move_inv),
]


def task1():
    text = "abcdefgh"
    for line in get_lines(fn):
        ic(text, line)
        for rx, oper, _ in cmds:
            if m := rx.match(line):
                text = oper(text, *m.groups())
                break
        else:
            print("unknown", line)
    ic(text)


def task2():
    text = "fbgdceah"
    lines = list(get_lines(fn))
    for line in lines[::-1]:
        ic(text, line)
        for rx, oper, oper_inv in cmds:
            if m := rx.match(line):
                text2 = oper_inv(text, *m.groups())
                if oper(text2, *m.groups()) != text:
                    ic("error", text2, text, line)
                text = text2
                break
        else:
            print("unknown", line)
    ic(text)
