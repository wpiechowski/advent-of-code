import random
import re
import time
from collections import deque

from tools import get_path, get_lines


def load():
    fn = get_path() + "i.txt"
    re_rule = re.compile(r"(\w+) => (\w+)")
    rules = []
    for line in get_lines(fn):
        line = line.strip()
        m = re_rule.match(line)
        if m:
            rules.append((m[1], m[2]))
        elif not line:
            continue
        else:
            return rules, line


def iter_subs(line, rule):
    rx = re.compile(rule[0])
    for m in rx.finditer(line):
        txt = line[:m.start()] + rule[1] + line[m.end():]
        yield txt


def iter_rev_subs(line, rule):
    rx = re.compile(rule[1])
    for m in rx.finditer(line):
        txt = line[:m.start()] + rule[0] + line[m.end():]
        yield txt


def task1():
    rules, input = load()
    them = set()
    for r in rules:
        print(r)
        for o in iter_subs(input, r):
            them.add(o)
    print(len(them))


def task2_():
    rules, target = load()
    found = set()
    q = deque([(target, 0)])
    t = time.time()
    while q:
        txt, steps = q.popleft()
        now = time.time()
        if now - t > 1:
            print(steps, len(q), len(found), len(txt))
            t = now
        if txt in found:
            continue
        found.add(txt)
        st2 = steps + 1
        for rule in rules:
            for t2 in iter_rev_subs(txt, rule):
                if t2 in found:
                    continue
                if t2 == "e":
                    print(st2)
                    return
                q.append((t2, st2))


def find(rules, src, target):
    if src == target:
        return 1
    if len(src) > len(target):
        return None
    print(src, target)
    for r_from, r_to in rules:
        if src.startswith(r_from):
            if target.startswith(r_to):
                r = find(rules, src[len(r_from):], target[len(r_to):])
                if r:
                    return r + 1
            else:
                r = find(rules, r_to + src[len(r_from):], target)
                if r:
                    return r + 1


def prefix(s1: str, s2: str):
    l = min(len(s1), len(s2))
    for i in range(l):
        if s1[i] == s2[i]:
            continue
        if s1[i].islower() ^ s2[i].islower():
            return i - 1
        return i
    return l


def find_back(rules, src, target):
    print(src, target)
    if src == target:
        return 1
    if len(src) > len(target):
        return None
    for r_from, r_to in rules:
        p = prefix(target, r_to)
        if p > 0:
            f = find_back(rules, r_to[p:], target[p:])
            if f:
                return f + 1


def task2__():
    rules, target = load()
    src = "e"
    r = find(rules, src, target)
    print(r)


def splits(txt: str, start: int = 1):
    for i in range(start, len(txt)):
        if txt[i].isupper():
            yield txt[:i], txt[i:]


def splits2(txt: str):
    for i in range(0, len(txt)):
        if txt[i].isupper():
            yield txt[:i], txt[i:]
    yield txt, ""


def split3(txt: str):
    prev = 0
    yield "", txt
    for i in range(len(txt)):
        if i == len(txt) - 1 or txt[i + 1].isupper():
            yield txt[prev: i + 1], txt[i + 1:]
            prev = i + 1


cache = {}
then = time.time()


def find_top2(rules, src: str, target: str, stack: str) -> int:
    global cache
    key = src, target, stack
    if key in cache:
        return cache[key]
    global then
    if stack == src and not target:
        return 0
    now = time.time()
    if now - then > 1:
        print(stack, src, target, len(cache))
        then = now
        if len(cache) > 10000000:
            cache = {}
    for new, tail in split3(target):
        stack += new
        for r_from, r_to in rules:
            if stack[-len(r_to):] == r_to:
                # print(stack, f"{r_from}=>{r_to}")
                stack2 = stack[:-len(r_to)] + r_from
                r = find_top2(rules, src, tail, stack2)
                if r is not None:
                    cache[key] = r + 1
                    return r + 1
    cache[key] = None


def find_random(rules, src: str) -> int:
    ret = 0
    target = "e"
    while target != src:
        random.shuffle(rules)
        for r_from, r_to in rules:
            if r_to in src:
                src = src.replace(r_to, r_from, 1)
                ret += 1
                print(len(src), src)
                break
    return ret


def task2():
    rules, target = load()
    src = "e"
    rules.sort(key = lambda x: len(x[1]), reverse=True)
    # r = find_top2(rules, src, target, "")
    r = find_random(rules, target)
    print(r)
