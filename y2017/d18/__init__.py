from tools import *


re_instr = r"(\w+) (-?[a-z0-9]+) ?(-?[a-z0-9]+)?"


def task1():
    code = list(get_re_lines("i.txt", re_instr))
    ic(code)
    freq = 0
    regs = {}
    pc = 0
    while 0 <= pc < len(code):
        instr, r1, r2 = code[pc]
        ic(regs, pc, code[pc])
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
        elif instr == "add":
            regs[r1] += r2
        elif instr == "snd":
            freq = regs[r1]
        elif instr == "mul":
            regs[r1] *= r2
        elif instr == "mod":
            regs[r1] %= r2
        elif instr == "rcv":
            if regs[r1]:
                regs[r1] = freq
                break
        if instr == "jgz":
            if r1.isalpha():
                cond = regs[r1]
            else:
                cond = int(r1)
            if cond > 0:
                pc += r2
            else:
                pc += 1
        else:
            pc += 1
    ic(freq)


def step(code, regs, q_in: list, q_out: list):
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
    elif instr == "add":
        regs[r1] += r2
    elif instr == "snd":
        if r1.isalpha():
            r1 = regs[r1]
        q_out.append(r1)
    elif instr == "mul":
        regs[r1] *= r2
    elif instr == "mod":
        regs[r1] %= r2
    elif instr == "rcv":
        if not q_in:
            return False
        regs[r1] = q_in.pop(0)
    if instr == "jgz":
        if r1.isalpha():
            cond = regs[r1]
        else:
            cond = int(r1)
        if cond > 0:
            pc += r2
        else:
            pc += 1
    else:
        pc += 1
    regs["pc"] = pc
    return True


def task2():
    code = list(get_re_lines("i.txt", re_instr))
    r1 = {"p": 1, "pc": 0}
    r2 = {"p": 0, "pc": 0}
    q1 = []
    q2 = []
    q1_adds = 0
    while True:
        # ic(r1, code[r1["pc"]], q2)
        l2 = len(q2)
        ret1 = step(code, r1, q1, q2)
        if len(q2) > l2:
            q1_adds += 1
        ret2 = step(code, r2, q2, q1)
        if not ret1 and not ret2:
            break
    ic(q1_adds)
