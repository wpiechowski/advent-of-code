from tools import *


class Gate:
    AND = lambda x, y: x and y
    OR = lambda x, y: x or y
    XOR = lambda x, y: bool(x ^ y)

    modes = {
        "AND": AND,
        "OR": OR,
        "XOR": XOR,
    }

    mode_names = {
        AND: "AND",
        OR: "OR",
        XOR: "XOR",
    }

    def __init__(self, nodes: dict[str, int], gates: dict, a: str, b: str, y: str, mode: callable):
        self.nodes = nodes
        self.gates = gates
        self.a = a
        self.b = b
        self.y = y
        self.renamed = ""
        self.mode = mode

    def calc(self) -> int:
        if self.nodes[self.a] is None:
            self.gates[self.a].calc()
        if self.nodes[self.b] is None:
            self.gates[self.b].calc()
        val = self.mode(self.nodes[self.a], self.nodes[self.b])
        self.nodes[self.y] = val
        return val

    def get_deps(self, active: bool, out: set):
        if self.y in out:
            return
        out.add(self.y)
        for n in (self.a, self.b):
            if n in out:
                continue
            if n not in self.gates:
                continue
            if not active or self.nodes[n] is None:
                self.gates[n].get_deps(active, out)

    def rename(self, n: str):
        if self.renamed:
            raise ValueError(f"{str(self)} already renamed from {self.y}")
        self.renamed = n
        print(str(self))

    def __str__(self):
        if self.a in self.gates:
            a = self.gates[self.a].y + "/" + self.gates[self.a].renamed
        else:
            a = self.a
        if self.b in self.gates:
            b = self.gates[self.b].y + "/" + self.gates[self.b].renamed
        else:
            b = self.b
        return f"{a} {self.mode_names[self.mode]} {b} -> {self.y}/{self.renamed}"

    def __repr__(self):
        return str(self)


def load(fn: str) -> tuple[dict, dict, int]:
    nodes = {}
    gates = {}
    max_z = 0
    re_gate = re.compile(r"([a-z0-9]+) ([A-Z]+) ([a-z0-9]+) -> ([a-z0-9]+)")
    for line in get_lines(fn):
        if ":" in line:
            node, val = line.split(": ")
            nodes[node] = int(val)
        elif m := re_gate.match(line):
            x1, mode, x2, y = m.groups()
            for n in (x1, x2, y):
                if n not in nodes:
                    nodes[n] = None
            gates[y] = Gate(nodes, gates, x1, x2, y, Gate.modes[mode])
            if y[0] == "z":
                max_z = max(max_z, int(y[1:]))
    return nodes, gates, max_z + 1


def task1():
    nodes, gates, n_z = load("i.txt")
    ret = 0
    print(n_z)
    for bit in range(n_z):
        name = f"z{bit:02}"
        val = gates[name].calc()
        ret |= val << bit
    print(ret)


def full_name(gates, name: str) -> [str, Gate]:
    for y, g in gates.items():
        if y == name or g.renamed == name:
            return f"{y}/{g.renamed}", g


def find_gate(gates: dict[str, Gate], a: str, b: str, mode_name: str) -> Gate:
    mode = Gate.modes[mode_name]
    for _, g in gates.items():
        if g.mode != mode:
            continue
        inputs = [g.a, g.b]
        for i in (g.a, g.b):
            if i in gates and gates[i].renamed:
                inputs.append(gates[i].renamed)
        if a in inputs and b in inputs:
            return g
    a, g1 = full_name(gates, a)
    b, g2 = full_name(gates, b)
    raise ValueError(f"gate not found {a} {mode_name} {b} ({g1}, {g2})")


def name(xyz: str, bit: int) -> str:
    return f"{xyz}{bit:02}"


def rename_chain(nodes, gates, bit: int, max_bit: int):
    g = find_gate(gates, name("x", bit), name("y", bit), "XOR")
    g.rename(name("ab", bit))
    if bit == 0:
        g = find_gate(gates, "x00", "y00", "AND")
        g.rename("c01")
    if bit > 0:
        g = find_gate(gates, name("c", bit), name("ab", bit), "XOR")
        n = name("z", bit)
        if g.y != n:
            raise ValueError(f"gate {g.y} expected {n}")
    if 0 < bit < max_bit - 1:
        g = find_gate(gates, name("ab", bit), name("c", bit), "AND")
        g.rename(name("e", bit))
        g = find_gate(gates, name("x", bit), name("y", bit), "AND")
        g.rename(name("f", bit))
        g = find_gate(gates, name("e", bit), name("f", bit), "OR")
        g.rename(name("c", bit+1))


def task2():
    nodes, gates, n_z = load("ii.txt")
    ret = 0
    print(n_z)
    for bit in range(n_z):
        name = f"z{bit:02}"
        o = set()
        gates[name].get_deps(True, o)
        print(bit, len(o), [str(gates[x]) for x in o])
        rename_chain(nodes, gates, bit, n_z - 1)
        print(bit, len(o), [str(gates[x]) for x in o])
        gates[name].calc()
