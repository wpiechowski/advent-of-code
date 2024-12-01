import re

from tools import *
import numpy as np


def load(fn: str):
    with open(get_path() + fn) as f:
        initial = next(f).strip()
        initial = initial.split(": ")[1]
        initial = np.array([0 if ch == "." else 1 for ch in initial])
        next(f)
        rules = np.zeros((32,), int)
        rx = re.compile(r"([.#]+) => ([.#])")
        try:
            while m := rx.match(next(f)):
                if m[2] == "#":
                    vals = [0 if ch == "." else 1 for ch in m[1]]
                    ndx = np.sum(2 ** np.arange(4, -1, -1) * vals)
                    rules[ndx] = 1
        except StopIteration:
            pass
    return initial, rules


def fix(state: np.array, offset: int) -> tuple[np.array, int]:
    step = 10
    if state[0] or state[1]:
        offset += step
        state = np.concatenate((np.zeros((step,), int), state))
    if state[-3]:
        state = np.concatenate((state, np.zeros((step,), int)))
    return state, offset


def evolve(state: np.array, offset: int, rules: np.array) -> tuple[np.array, int]:
    ret = np.zeros(state.shape, int)
    cur = 0
    for n, v in enumerate(state[2:]):
        cur = (cur << 1) & 0b11111 | v
        ret[n] = rules[cur]
    return ret, offset


def to_str(state: np.array) -> str:
    return "".join(["#" if v else "." for v in state])


def task1():
    fn = "i.txt"
    state, rules = load(fn)
    offset = 0
    state, offset = fix(state, offset)
    print("  0", offset, to_str(state))
    for step in range(200):
        state, offset = fix(state, offset)
        state, offset = evolve(state, offset, rules)
        print(f"{step + 1:>3}", offset, to_str(state))
    ret = 0
    for n, v in enumerate(state):
        ret += v * (n - offset)
    print(ret)
    # task2
    ret = 0
    t = 50000000000
    offset -= t - (step + 1)
    for n, v in enumerate(state):
        ret += v * (n - offset)
    print(ret)


"""
task2:
gen 200 is stable, just shifting
"""