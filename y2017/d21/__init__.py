from itertools import product

from tools import *
import numpy as np
from dataclasses import dataclass


@dataclass
class Rule:
    input: np.array
    output: np.array

    def is_match(self, other: np.array):
        if self.input.shape != other.shape:
            return False
        for o in (other, other.T):
            oo = o.copy()
            for r in range(4):
                if np.all(np.rot90(oo, r) == self.input):
                    return True
        return False


def parse_matrix(t: str) -> np.array:
    lines = t.split("/")
    ret = np.zeros((len(lines), len(lines)), int)
    for y, line in enumerate(lines):
        ret[y, :] = [ch == "#" for ch in line]
    return ret


def load():
    fn = "i.txt"
    rx = r"([.#/]+) => ([.#/]+)"
    rules = []
    for a, b in get_re_lines(fn, rx):
        a = parse_matrix(a)
        b = parse_matrix(b)
        r = Rule(a, b)
        rules.append(r)
    return rules


def step(board: np.array, rules: list[Rule]) -> np.array:
    s = board.shape[0]
    if s % 2 == 0:
        step_i = 2
        step_o = 3
    else:
        step_i = 3
        step_o = 4
    ss = s * step_o // step_i
    ret = np.zeros((ss, ss), int)
    for ny, nx in product(range(s // step_i), repeat=2):
        xi = nx * step_i
        yi = ny * step_i
        xo = nx * step_o
        yo = ny * step_o
        sub_i = board[yi: yi + step_i, xi: xi + step_i]
        sub_o = ret[yo: yo + step_o, xo: xo + step_o]
        for rule in rules:
            if rule.is_match(sub_i):
                sub_o[:, :] = rule.output
                break
        else:
            raise ValueError("no rule for %s" % sub_i)
    return ret


def task1():
    rules = load()
    board = np.array([
        [0, 1, 0],
        [0, 0, 1],
        [1, 1, 1]])
    for i in range(18):
        ic(i, board.shape)
        board = step(board, rules)
    # ic(board)
    ic(np.sum(board))
