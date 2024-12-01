from tools import *
from dataclasses import dataclass


@dataclass
class State:
    name: str
    actions: list[tuple[int, int, str]] = ()


def get_state(src) -> State:
    s = State(next(src)[-3])
    actions = []
    for _ in range(2):
        next(src)
        write_val = int(next(src)[-3])
        move = 1 if next(src)[-4] == "h" else -1
        new_state = next(src)[-3]
        actions.append((write_val, move, new_state))
    s.actions = tuple(actions)
    return s


def load():
    fn = "i.txt"
    states = {}
    with open(get_path() + fn) as f:
        s0 = next(f)[-3]
        cnt = int(next(f).split(" ")[-2])
        next(f)
        ic(s0, cnt)
        try:
            while s := get_state(f):
                states[s.name] = s
                next(f)
        except StopIteration:
            pass
    return states, s0, cnt


def task1():
    states, s0, count = load()
    ic(states, s0, count)
    pos = 0
    tape = [0]
    state = s0
    increment = 10
    for i in range(count):
        action = states[state].actions[tape[pos]]
        tape[pos] = action[0]
        pos += action[1]
        state = action[2]
        if pos >= len(tape):
            tape.extend([0] * increment)
            ic(i, len(tape))
        if pos < 0:
            tape = [0] * increment + tape
            pos += increment
            ic(i, len(tape))
    ret = sum(tape)
    ic(ret)
