import re


re_card = re.compile(r"Card ([0-9 ]+): ([0-9 ]+) \| ([0-9 ]+)")


def parse_ints(line: str) -> list[int]:
    ret = []
    for x in range(0, len(line), 3):
        if line[x] == " ":
            ret.append(int(line[x+1]))
        else:
            ret.append(int(line[x:x+2]))
    return ret


def check_line(line: str) -> int:
    m = re_card.match(line)
    wins = set(parse_ints(m.group(2)))
    hand = set(parse_ints(m.group(3)))
    match = wins & hand
    # print(line, match)
    return len(match)


def task1():
    pts = 0
    for line in open("i04a.txt"):
        line = line.strip()
        pts += int(2 ** (check_line(line) - 1))
    print(pts)


def task2():
    mults = []
    total = 0
    for line in open("i04a.txt"):
        line = line.strip()
        print(line, mults)
        if not mults:
            mul = 1
        else:
            mul = mults[0]
            mults = mults[1:]
        pts = check_line(line)
        total += mul
        for n in range(pts):
            while len(mults) <= n:
                mults.append(1)
            mults[n] += mul
    print(total)
