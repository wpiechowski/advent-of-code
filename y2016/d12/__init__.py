import time

from tools import get_re_lines

fn = "i.txt"
re_line = r"(cpy|inc|dec|jnz) ([a-d0-9]+)( ([a-d0-9\-]+))?"


def task1():
    code = []
    for instr, r1, _, r2 in get_re_lines(fn, re_line):
        code.append((instr, r1, r2))
    regs = {x: 0 for x in "abcd"}
    regs["c"] = 1   # task2
    pc = 0
    tp = time.time()
    steps = 0
    while 0 <= pc < len(code):
        steps += 1
        instr, r1, r2 = code[pc]
        now = time.time()
        if now - tp >= 1:
            tp = now
            print(steps, regs, pc, instr, r1, r2)
        if instr == "cpy":
            regs[r2] = int(regs.get(r1, r1))
            pc += 1
        elif instr == "inc":
            regs[r1] += 1
            pc += 1
        elif instr == "dec":
            regs[r1] -= 1
            pc += 1
        elif instr == "jnz":
            val = int(regs.get(r1, r1))
            dif = int(r2)
            if val:
                pc += dif
            else:
                pc += 1
    ic(regs)
