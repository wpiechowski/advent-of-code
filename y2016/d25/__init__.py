import time

from tools import get_re_lines

fn = "i.txt"
re_line = r"(cpy|inc|dec|jnz|out|adz|nop) ?([a-d0-9\-]+)( ([a-d0-9\-]+))?"


def check(code, a: int):
    regs = {x: 0 for x in "abcd"}
    regs["a"] = a
    pc = 1
    sig = []
    tp = time.time()
    steps = 0
    state_1 = None
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
        elif instr == "out":
            val = int(regs.get(r1, r1))
            if val not in (0, 1):
                print("wrong value")
                return False
            sig.append(val)
            prev = 1 - sig[0]
            for s in sig:
                if s == prev:
                    print("not clock")
                    return False
                prev = s
            if val == 1:
                cur_state = pc, regs["a"], regs["b"], regs["c"], regs["d"]
                if not state_1 or len(sig) < 100:
                    state_1 = cur_state
                else:
                    cmp = state_1 == cur_state
                    if not cmp:
                        print("different state")
                    return cmp
            pc += 1
        elif instr == "nop":
            pc += 1
    ic(regs)


def task1():
    code = [None]
    for instr, r1, _, r2 in get_re_lines(fn, re_line):
        code.append([instr, r1, r2])
    for a in range(10000):
        print(a)
        r = check(code, a)
        if r:
            break
