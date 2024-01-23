from tools import get_re_lines

fn = "i.txt"

vals = {
    "children": (3, 0),
    "cats": (7, 1),
    "samoyeds": (2, 0),
    "pomeranians": (3, -1),
    "akitas": (0, 0),
    "vizslas": (0, 0),
    "goldfish": (5, -1),
    "trees": (3, 1),
    "cars": (2, 0),
    "perfumes": (1, 0),
}

re_line = r"Sue (\d+): (\w+): (\d+), (\w+): (\d+), (\w+): (\d+)"


def task1():
    for sue in get_re_lines(fn, re_line):
        for name, val in zip(sue[1::2], sue[2::2]):
            if vals[name][0] != int(val):
                break
        else:
            print(sue[0])


def task2():
    for sue in get_re_lines(fn, re_line):
        for name, val in zip(sue[1::2], sue[2::2]):
            mode = vals[name][1]
            val = int(val)
            if mode == 0 and vals[name][0] != int(val):
                break
            if mode == 1 and val <= vals[name][0]:
                break
            if mode == -1 and val >= vals[name][0]:
                break
        else:
            print(sue[0])
