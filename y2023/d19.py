import re


class Rule:
    re_rule = re.compile(r"(([xmas])([<>])(\d+):)?([a-z]+|[RA])")

    def __init__(self, val: str):
        m = self.re_rule.match(val)
        self.var = m[2]
        self.gt = 1 if m[3] == ">" else -1
        self.val = int(m[4]) if m[1] else None
        self.result = m[5]

    def compare(self, val: int):
        if not self.var:
            return True
        if self.gt > 0:
            return val > self.val
        else:
            return val < self.val

    def insert_range(self, part_range: dict[str, tuple[int, int]]) -> list[tuple[str, dict[str, tuple[int, int]]]]:
        if self.var:
            vr = part_range[self.var]
            c1 = self.compare(vr[0])
            c2 = self.compare(vr[1])
            if not c1 and not c2:
                return [("pass", part_range)]
            if c1 and c2:
                return [(self.result, part_range)]
            pr2 = part_range.copy()
            if c1:
                part_range[self.var] = (vr[0], self.val - 1)
                pr2[self.var] = (self.val, vr[1])
                return [
                    (self.result, part_range),
                    ("pass", pr2),
                ]
            else:
                part_range[self.var] = (vr[0], self.val)
                pr2[self.var] = (self.val + 1, vr[1])
                return [
                    ("pass", part_range),
                    (self.result, pr2),
                ]
        else:
            return [(self.result, part_range)]


class Workflow:
    def __init__(self, val: str):
        self.rules = list(map(Rule, val.split(",")))

    def insert_part(self, part: dict) -> str:
        for r in self.rules:
            if r.var:
                if part[r.var] * r.gt > r.val * r.gt:
                    return r.result
            else:
                return r.result


def get_part(val: str) -> dict:
    vals = val.split(",")
    ret = {}
    for v in vals:
        name, i = v.split("=")
        ret[name] = int(i)
    return ret


def load(fn):
    workflows = {}
    parts = []
    re_workflow = re.compile(r"([a-z]+){(.+)}")
    re_part = re.compile(r"{(.+)}")
    for line in open(fn):
        line = line.strip()
        m = re_workflow.match(line)
        if m:
            w = Workflow(m[2])
            workflows[m[1]] = w
        m = re_part.match(line)
        if m:
            part = get_part(m[1])
            parts.append(part)
    return workflows, parts


def pass_part(workflows: dict[str, Workflow], part: dict) -> str:
    cur_wf = "in"
    while True:
        w = workflows[cur_wf]
        r = w.insert_part(part)
        if r in ("R", "A"):
            return r
        cur_wf = r


def task1():
    fn = "i19a.txt"
    score = 0
    workflows, parts = load(fn)
    for part in parts:
        r = pass_part(workflows, part)
        if r == "A":
            score += part["x"] + part["m"] + part["a"] + part["s"]
    print(score)


def calc_combs(workflows: dict[str, Workflow]) -> int:
    queue = [
        ("in", 0, {"x": (1, 4000), "m": (1, 4000), "a": (1, 4000), "s": (1, 4000)}),
    ]
    combs = 0
    while queue:
        cur = queue.pop()
        wf = workflows[cur[0]]
        pr = cur[2]
        rule = wf.rules[cur[1]]
        prs = rule.insert_range(pr)
        for res, p in prs:
            if res == "A":
                c = 1
                for val_min, val_max in p.values():
                    c *= val_max - val_min + 1
                combs += c
            elif res == "pass":
                queue.append((cur[0], cur[1] + 1, p))
            elif res != "R":
                queue.append((res, 0, p))
    return combs


def task2():
    fn = "i19a.txt"
    score = 0
    workflows, _ = load(fn)
    ret = calc_combs(workflows)
    print(ret)
