from tools import *


class Computer:
    def __init__(self, code: list[int], input):
        self.code = code
        self.pc = 0
        self.input = iter(input)
        self.output = []

    def step(self):
        op = self.code[self.pc]
        modes = ((op // 100) % 10) + 2 * (op // 1000)
        op = op % 100

        # ic(self.pc, op, modes)
        def arg(n: int) -> int:
            return self.code[self.pc + n]

        def argm(n: int) -> int:
            a = arg(n)
            if not modes & (1 << (n - 1)):
                a = self.code[a]
            return a

        if op in (1, 2):
            if op == 1:
                res = argm(1) + argm(2)
            else:
                res = argm(1) * argm(2)
            ptr = arg(3)
            self.code[ptr] = res
            self.pc += 4
        elif op in (3, 4):
            if op == 3:
                self.code[arg(1)] = next(self.input)
            else:
                self.output.append(argm(1))
            self.pc += 2
        elif op == 5:
            if argm(1):
                self.pc = argm(2)
            else:
                self.pc += 3
        elif op == 6:
            if not argm(1):
                self.pc = argm(2)
            else:
                self.pc += 3
        elif op == 7:
            self.code[arg(3)] = int(argm(1) < argm(2))
            self.pc += 4
        elif op == 8:
            self.code[arg(3)] = int(argm(1) == argm(2))
            self.pc += 4
        elif op == 99:
            return -1
        else:
            raise ValueError(f"invalid opcode {op}")
        return 0

    def run(self):
        while self.step() >= 0:
            pass


def task1():
    code = list(get_int_lines("i.txt"))[0]
    input = [1]
    c = Computer(code, input)
    c.run()
    ic(c.output, c.pc)
    # ic(c.code)


def task2():
    code = list(get_int_lines("i.txt"))[0]
    # code = [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]
    input = [5]
    c = Computer(code, input)
    c.run()
    ic(c.output, c.pc)
    # ic(c.code)
