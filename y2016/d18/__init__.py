from collections import Counter

# seed = ".^^.^.^^^^"
seed = ".^^^.^.^^^.^.......^^.^^^^.^^^^..^^^^^.^.^^^..^^.^.^^..^.^..^^...^.^^.^^^...^^.^.^^^..^^^^.....^...."
total_rows = 400000


def step(x: str) -> str:
    ret = ""
    for c1, c2 in zip("." + x[:-1], x[1:] + "."):
        ret += "." if c1 == c2 else "^"
    return ret


def task1():
    row = seed
    print(row)
    c = Counter(row)
    for n in range(total_rows - 1):
        print(n)
        row = step(row)
        c.update(row)
        # print(row)
    print(c)
