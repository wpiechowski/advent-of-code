from tools import get_re_lines

fn = "i.txt"
re_line = r"(hlf|tpl|inc|jmp|jie|jio) (a|b|[+\-0-9]+)(, ([+\-0-9]+))?"


def task1():
    lines = list(get_re_lines(fn, re_line))
    pc = 0
    regs = {
        "a": 1, # task2: 1
        "b": 0,
    }
    while 0 <= pc < len(lines):
        opcode, p1, _, p2 = lines[pc]
        print(pc, regs["a"], regs["b"], opcode, p1, p2)
        if opcode == "hlf":
            regs[p1] //= 2
            pc += 1
        elif opcode == "tpl":
            regs[p1] *= 3
            pc += 1
        elif opcode == "inc":
            regs[p1] += 1
            pc += 1
        elif opcode == "jmp":
            pc += int(p1)
        elif opcode == "jie":
            if regs[p1] & 1 == 0:
                pc += int(p2)
            else:
                pc += 1
        elif opcode == "jio":
            if regs[p1] == 1:
                pc += int(p2)
            else:
                pc += 1
    print(pc, regs)
