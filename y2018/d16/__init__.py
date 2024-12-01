from tools import *
import operator
import numpy as np

# 2: A always reg, B reg/imm
# 3: IR, RI, RR

operations = [
    ("add", 2, operator.add),
    ("mul", 2, operator.mul),
    ("ban", 2, operator.and_),
    ("bor", 2, operator.or_),
    ("set", 1, lambda a, b: a),
    ("gt", 3, operator.gt),
    ("eq", 3, operator.eq),
]


def iter_instrs(before: list[int], instr: list[int]):
    for name, mode, func in operations:
        if mode == 1:
            for name2, a in zip("ir", (instr[1], before[instr[1]])):
                yield name + name2, func, instr[0], a, None
        elif mode == 2:
            for name2, b in zip("ir", (instr[2], before[instr[2]])):
                yield name + name2, func, instr[0], before[instr[1]], b
        elif mode == 3:
            a_ = instr[1]
            b_ = instr[2]
            for name2, a, b in zip(("ir", "ri", "rr"), (a_, before[a_], before[a_]), (before[b_], b_, before[b_])):
                yield name + name2, func, instr[0], a, b


def test_instr(before: list[int], instr: list[int], after: list[int]) -> tuple[int, list[str]]:
    valids = 0
    names = []
    for n, (r1, r2) in enumerate(zip(before, after)):
        if r1 != r2 and n != instr[-1]:
            raise ValueError("wrong reg differs")
    for name, func, opcode, a, b in iter_instrs(before, instr):
        c = func(a, b)
        if c == after[instr[-1]]:
            valids += 1
            names.append(name)
            # ic(before, instr, after, name, a, b, c)
    return valids, names


def task1_():
    before = [3, 2, 1, 1]
    instr = [9, 2, 1, 2]
    after = [3, 2, 2, 1]
    test_instr(before, instr, after)


def task1():
    before = []
    instr = []
    after = []
    zz = False
    ret = 0
    for line in get_lines("i.txt"):
        vals = row_of_ints(line)
        if line.startswith("Before"):
            before = vals
            zz = True
        elif line.startswith("After"):
            after = vals
            zz = False
            t, _ = test_instr(before, instr, after)
            ret += t >= 3
        elif zz:
            instr = vals
    ic(ret)


def task2():
    names = [
        "addr", "addi",
        "mulr", "muli",
        "banr", "bani",
        "borr", "bori",
        "setr", "seti",
        "gtir", "gtri", "gtrr",
        "eqir", "eqri", "eqrr",
    ]
    name_id = {name: n for n, name in enumerate(names)}
    op_map = np.ones((16, len(names)), int)
    before = []
    instr = []
    after = []
    program = []
    state = 0
    for line in get_lines("i.txt"):
        vals = row_of_ints(line)
        if line.startswith("Before"):
            before = vals
            state = 1
        elif line.startswith("After"):
            after = vals
            state = 0
            t, n = test_instr(before, instr, after)
            # ic(instr, n)
            if t == 0:
                raise ValueError("unable to match")
            for n2 in names:
                if n2 not in n:
                    op_map[instr[0], name_id[n2]] = 0
        elif state == 1:
            instr = vals
        elif len(vals) == 4:
            program.append(vals)
    ops = {}    # op -> name index
    while True:
        # find single
        for op, line in enumerate(op_map):
            if op in ops:
                continue
            if sum(line) == 1:
                fnd = np.argmax(line)
                for op2 in range(16):
                    if op2 != op:
                        op_map[op2, fnd] = 0
                ops[op] = fnd
                break
        else:
            break
    ic(ops)
    regs = [0, 0, 0, 0]
    for line in program:
        for name, func, opcode, a, b in iter_instrs(regs, line):
            if name != names[ops[opcode]]:
                continue
            ic(regs, name, line)
            regs[line[-1]] = func(a, b)
    ic(regs)
