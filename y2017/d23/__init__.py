import time

from tools import *


re_instr = r"(\w+) (-?[a-z0-9]+) ?(-?[a-z0-9]+)?"

def step(code, regs):
    pc = regs["pc"]
    if pc < 0 or pc >= len(code):
        ic("jump out")
        return False
    instr, r1, r2 = code[pc]
    if r1 not in regs:
        regs[r1] = 0
    if r2 and r2.isalpha():
        if r2 not in regs:
            regs[r2] = 0
        r2 = regs[r2]
    elif r2:
        r2 = int(r2)
    if instr == "set":
        regs[r1] = r2
    elif instr == "sub":
        regs[r1] -= r2
    elif instr == "mul":
        regs[r1] *= r2
        regs["mul"] += 1
    if instr == "jnz":
        if r1.isalpha():
            cond = regs[r1]
        else:
            cond = int(r1)
        if cond != 0:
            pc += r2
        else:
            pc += 1
    else:
        pc += 1
    regs["pc"] = pc
    return True


def task1():
    code = list(get_re_lines("i.txt", re_instr))
    regs = {"mul": 0, "pc": 0}
    while step(code, regs):
        pass
    ic(regs)


def task2_slow():
    code = list(get_re_lines("i.txt", re_instr))
    regs = {"mul": 0, "pc": 0, "a": 1}
    t = time.time()
    while step(code, regs):
        now = time.time()
        if now - t > 1:
            t = now
            print(regs)
    ic(regs)


def task2():
    program()


def program():
    a = 1
    b = 0
    c = 0
    fac1 = 0
    fac2 = 0
    not_found = 0
    h = 0
    muls = 0

    b = 79
    c = b
    if a:
        b = 79 * 100 + 100000   # 107900
        c = 17000 + 79 * 100 + 100000   # 124900
    while True:
        not_found = 1
        fac1 = 2
        while True:
            if b % fac1 == 0:
                not_found = 0
            # fac2 = 2
            # while True:
            #     if fac1 * fac2 == b:
            #         not_found = 0
            #     fac2 += 1
            #     if fac2 == b:
            #         break
            fac1 += 1
            if fac1 == b:
                break
        if not not_found:
            h += 1
            ic(b, c, h)
        if b == c:
            break
        b += 17
    ic(muls)
