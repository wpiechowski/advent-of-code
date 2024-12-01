import time

from tools import get_re_lines

fn = "i.txt"
re_line = r"(cpy|inc|dec|jnz|tgl) ([a-d0-9\-]+)( ([a-d0-9\-]+))?"


def task1():
    code = [None]
    subs = {
        "inc": "dec",
        "dec": "inc",
        "tgl": "inc",
        "jnz": "cpy",
        "cpy": "jnz",
    }
    for instr, r1, _, r2 in get_re_lines(fn, re_line):
        code.append([instr, r1, r2])
    regs = {x: 0 for x in "abcd"}
    regs["a"] = 12
    pc = 1
    tp = time.time()
    steps = 0
    while 1 <= pc < len(code):
        steps += 1
        instr, r1, r2 = code[pc]
        # ic(pc, regs, code[pc])
        now = time.time()
        if now - tp >= 1:
            tp = now
            print(steps, regs, pc, instr, r1, r2)
        if instr == "cpy":
            if r2 in "abcd":
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
            dif = int(regs.get(r2, r2))
            if val:
                pc += dif
            else:
                pc += 1
        elif instr == "tgl":
            off = int(regs.get(r1, r1))
            if 1 <= pc + off < len(code):
                target = code[pc + off]
                target[0] = subs[target[0]]
            pc += 1
    ic(regs)
