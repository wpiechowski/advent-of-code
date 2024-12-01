from tools import *
import operator


def load():
    conds = {
        "==": operator.__eq__,
        ">": operator.__gt__,
        "<": operator.__lt__,
        ">=": operator.__ge__,
        "<=": operator.__le__,
        "!=": operator.__ne__,
    }
    fn = "i.txt"
    re_line = r"(\w+) (inc|dec) (-?\d+) if (\w+) ([=<>!]+) (-?\d+)"
    for r1, mode, amt, r2, cond, thr in get_re_lines(fn, re_line):
        amt = int(amt)
        if mode == "dec":
            amt = -amt
        thr = int(thr)
        yield r1, amt, r2, conds[cond], thr


def task1():
    regs = {}
    temp_max = 0
    for r1, amt, r2, cond, thr in load():
        if r1 not in regs:
            regs[r1] = 0
        if r2 not in regs:
            regs[r2] = 0
        r2 = regs[r2]
        if cond(r2, thr):
            regs[r1] += amt
        temp_max = max(temp_max, *regs.values())
    ic(regs)
    ic(max(regs.values()), temp_max)
