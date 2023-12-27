import re


def process(line: str):
    nums = list(filter(lambda x: ord("0") <= ord(x) <= ord("9"), line))
    return int(nums[0] + nums[-1])


digits = [
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
]


re_dig = re.compile(r".*[0-9].*")


def preprocess0(line: str):
    while True:
        best_n = -1
        best_pos = len(line)
        for n, name in enumerate(digits):
            f = line.find(name)
            if f == -1:
                continue
            if f < best_pos:
                best_pos = f
                best_n = n
        if best_n < 0:
            return line
        line = line.replace(digits[best_n], str(best_n), 1)


def process2(line: str):
    for n in range(len(line)):
        if ord("0") <= ord(line[n]) <= ord("9"):
            first = line[n]
            break
        for nd, d in enumerate(digits):
            if line[n:].startswith(d):
                first = str(nd)
                break
        else:
            continue
        break
    for n in reversed(range(len(line))):
        if ord("0") <= ord(line[n]) <= ord("9"):
            last = line[n]
            break
        for nd, d in enumerate(digits):
            if line[n:].startswith(d):
                last = str(nd)
                break
        else:
            continue
        break
    return int(first + last)


def task1():
    val = 0
    for line in open("i01a.txt"):
        line = line.strip()
        # line2 = preprocess(line)
        v = process2(line)
        val += v
        print(line, v)
    print(val)
