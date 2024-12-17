from tools import *
from typing import List


@dataclass
class State:
    ABC: List[int]
    PC: int = 0


def load(fn: str) -> tuple[State, list[int]]:
    re_reg = re.compile(r"Register ([A-C]): (\d+)")
    s = State([0, 0, 0])
    for line in get_lines(fn):
        if not line:
            continue
        if line[0] == "P":
            return s, row_of_ints(line)
        elif m := re_reg.match(line):
            val = int(m[2])
            n = ord(m[1]) - ord("A")
            s.ABC[n] = val


def step(state: State, code: list[int]) -> int:
    if state.PC >= len(code):
        return -2
    ret = -1
    op = code[state.PC]
    arg = code[state.PC + 1]
    state.PC += 2

    def combo():
        if arg <= 3:
            return arg
        elif arg == 7:
            raise ValueError("invalid combo")
        else:
            return state.ABC[arg - 4]

    if op == 0:
        den = combo()
        state.ABC[0] >>= den
    elif op == 1:
        state.ABC[1] ^= arg
    elif op == 2:
        state.ABC[1] = combo() & 7
    elif op == 3:
        if state.ABC[0]:
            state.PC = arg
    elif op == 4:
        state.ABC[1] ^= state.ABC[2]
    elif op == 5:
        ret = combo() & 7
    elif op == 6:
        state.ABC[1] = state.ABC[0] >> combo()
    elif op == 7:
        state.ABC[2] = state.ABC[0] >> combo()
    else:
        raise ValueError("bad instr")
    return ret


def task1():
    state, code = load("i.txt")
    print(state)
    print(code)
    ret = []
    while (val := step(state, code)) != -2:
        if val >= 0:
            print(val)
            ret.append(str(val))
    print(",".join(ret))


def test_code(code: list[int], a0: int, count: int, loud: bool = False):
    state = State([a0, 0, 0], 0)
    out = []
    for i in range(1000000):
        r = step(state, code)
        if r == -2:
            return False
        if r >= 0:
            out.append(r)
            if loud:
                print(r)
            if r != code[len(out) - 1]:
                return False
            if len(out) == count:
                return True
    return False


def test_fast(code: list[int], a: int, count: int):
    here = 0
    while True:
        b = (a & 7) ^ 5
        c = a >> b
        b = (b ^ c ^ 6) & 7
        if b != code[here]:
            return False
        a >>= 3
        here += 1
        if count == here:
            return True


def gen_trials():
    ret = [set(), set(), set(), set(), set(), set(), set(), set()]
    for a in range(1 << 12):
        b = (a & 7) ^ 5
        c = a >> b
        mask = (0b111 << b) | 0b111
        b = (b ^ c ^ 6) & 7
        ret[b].add((a & mask, mask))
    return ret


def find_A(code: list[int], good: int, a: int, fixed: int, mask: int, trials, hist: list[int]):
    ab = bin(a)
    mb = bin(mask)
    # print(f"attempt {good=} {fixed=} {hist} a={ab[2:-fixed]}|{ab[-fixed:]} mask={mb[2:-fixed]}|{mb[-fixed:]}")
    for k, m in trials[code[good]]:
        aa = a | (k << fixed)
        if (a & mask) != (aa & mask):
            continue
        if test_fast(code, aa, good + 1):
            if good + 1 == len(code):
                yield aa
            else:
                yield from find_A(code, good + 1, aa, fixed + 3, mask | (m << fixed), trials, hist + [k])


def task2():
    code = [2, 4, 1, 5, 7, 5, 4, 3, 1, 6, 0, 3, 5, 5, 3, 0]
    t = gen_trials()
    ret = min(find_A(code, 0, 0, 0, 0, t, []))
    print(ret)
