import re
from itertools import chain


def node_names(nodes):
    return ",".join(map(lambda x: x.name, nodes))


class Node:
    def __init__(self, name: str, mode: str):
        self.name = name
        self.mode = mode
        self.inputs = []
        self.outputs = []
        self.input_vals = {}
        self.cur_val = False

    def __str__(self):
        return f"{self.mode}{self.name}[{node_names(self.inputs)}]->[{node_names(self.outputs)}]"

    def input_from(self, in_name: str, val: bool) -> list[tuple[str, str, bool]]:
        ret = []
        if self.mode == "":
            for o in self.outputs:
                ret.append((self.name, o.name, val))
        elif self.mode == "%":
            if not val:
                self.cur_val = not self.cur_val
                for o in self.outputs:
                    ret.append((self.name, o.name, self.cur_val))
        elif self.mode == "&":
            if not self.input_vals:
                for i in self.inputs:
                    self.input_vals[i.name] = False
            self.input_vals[in_name] = val
            all_hi = True
            for v in self.input_vals.values():
                if not v:
                    all_hi = False
                    break
            for o in self.outputs:
                ret.append((self.name, o.name, not all_hi))
        return ret


def load(fn):
    nodes = {
        "button": Node("button", ""),
    }
    links = []
    re_line = re.compile(r"([%&])?([a-z]+) -> (.+)")
    for line in open(fn):
        m = re_line.match(line.strip())
        if m:
            node_name = m[2]
            nodes[node_name] = Node(node_name, m[1] or "")
            for o in m[3].split(", "):
                links.append((node_name, o))
    for a, b in chain(links, [("button", "broadcaster")]):
        if b not in nodes:
            nodes[b] = Node(b, "")
        na = nodes[a]
        nb = nodes[b]
        na.outputs.append(nb)
        nb.inputs.append(na)
    return nodes


def push_button(nodes: dict[str, Node]):
    pulses_hi = 0
    pulses_lo = 0
    pulses = [("button", "broadcaster", False)]
    while pulses:
        src_name, name, val = pulses.pop(0)
        # print(f"{src_name} -{'high' if val else 'low'}-> {name}")
        if val:
            pulses_hi += 1
        else:
            pulses_lo += 1
        outs = nodes[name].input_from(src_name, val)
        pulses.extend(outs)
    return pulses_lo, pulses_hi


def task1():
    fn = "i20a.txt"
    nodes = load(fn)
    # for node in nodes.values():
    #     print(node)
    pulses_hi = 0
    pulses_lo = 0
    for cnt in range(1000):
        pl, ph = push_button(nodes)
        pulses_lo += pl
        pulses_hi += ph
        print(cnt + 1, pl, ph, pulses_lo, pulses_hi)
    print(pulses_lo, pulses_hi, pulses_lo * pulses_hi)
