from tools import *


class Computer:
    def __init__(self, code: list[int], input):
        self.code = code
        self.pc = 0
        self.input = input
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
                self.code[arg(1)] = self.input[0]
                self.input = self.input[1:]
                self.pc += 2
            else:
                val = argm(1)
                self.output.append(val)
                self.pc += 2
                return 1, val
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
            return 0, -1
        else:
            raise ValueError(f"invalid opcode {op}")
        return 0, 0

    def run(self):
        while self.step() != (0, -1):
            pass

    def run_iter(self):
        while True:
            a, b = self.step()
            if (a, b) == (0, -1):
                return
            if a == 1:
                yield b


def task1():
    code = list(get_int_lines("i.txt"))[0]
    best = 0
    best_ph = None
    for ids in permutations(range(5), 5):
        passed = 0
        for i in ids:
            comp = Computer(code.copy(), [i, passed])
            comp.run()
            passed = comp.output[-1]
        if passed > best:
            best = passed
            best_ph = ids
        # print(ids, passed)
    print(best_ph, best)


def task2():
    code = list(get_int_lines("i.txt"))[0]
    best = 0
    best_ph = None
    for ids in permutations(range(5, 10), 5):
        comps = [Computer(code.copy(), [i]) for i in ids]
        iters = [comp.run_iter() for comp in comps]
        counts = 0
        try:
            passed = 0
            cur = 0
            while True:
                comps[cur].input.append(passed)
                passed = next(iters[cur])
                cur = (cur + 1) % len(comps)
                counts += 1
        except StopIteration:
            pass
        passed = comps[-1].output[-1]
        if passed > best:
            best = passed
            best_ph = ids
        print(ids, counts, passed)
    print(best_ph, best)
