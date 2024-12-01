from tools import *


def load(fn: str):
    rx = r"Step (\w+) must be finished before step (\w+) can begin"
    return list(get_re_lines(fn, rx))


def find_ready(rules: list[tuple[str, str]], done: set[str]):
    ret = set()
    unret = set()
    for a, b in rules:
        if a in done and b not in done:
            ret.add(b)
        if a not in done and b not in done:
            unret.add(b)
    return list(ret - unret)


def add_firsts(rules: list):
    nodes = set()
    for a, b in rules:
        nodes.add(a)
        nodes.add(b)
    for n in nodes:
        rules.append(("^", n))


def task1():
    rules = load("s.txt")
    ic(rules)
    add_firsts(rules)
    done = ["^"]
    while True:
        f = find_ready(rules, done)
        if not f:
            break
        ic(done, f)
        f.sort()
        done.append(f[0])
    r = "".join(done)
    ic(r)


def find_ready2(rules: list[tuple[str, str]], done: set[str], busy: set[str]):
    ret = set()
    unret = busy.copy()
    for a, b in rules:
        if a in done and b not in done:
            ret.add(b)
        if a not in done and b not in done:
            unret.add(b)
    return sorted(list(ret - unret))


def task2():
    rules = load("i.txt")
    add_firsts(rules)
    n_workers = 10
    penalty = 60
    done = {"^"}
    busy = set()
    # done_time, task
    work = [[0, "^"] for _ in range(n_workers)]
    now = 0
    while True:
        work.sort()
        now = work[0][0]
        done.add(work[0][1])
        if work[0][1] in busy:
            ic(work, done, busy)
            busy.remove(work[0][1])
        f = find_ready2(rules, done, busy)
        if not f and not busy:
            ic(now)
            break
        if not f:
            work[0][0] += 1
            work[0][1] = "^"
        else:
            work[0][1] = f[0]
            work[0][0] = ord(f[0]) - ord("A") + 1 + penalty + now
            busy.add(f[0])
