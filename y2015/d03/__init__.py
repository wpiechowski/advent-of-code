def task1():
    fn = "y2015/d03/i.txt"
    x, y = 0, 0
    visits = {(x, y)}
    for line in open(fn):
        for ch in line:
            if ch == ">":
                x += 1
            elif ch == "<":
                x -= 1
            elif ch == "v":
                y -= 1
            elif ch == "^":
                y += 1
            visits.add((x, y))
        print(len(visits))


def update(x, y, ch):
    if ch == ">":
        x += 1
    elif ch == "<":
        x -= 1
    elif ch == "v":
        y -= 1
    elif ch == "^":
        y += 1
    return x, y


def task2():
    fn = "y2015/d03/i.txt"
    pos = ((0, 0), (0, 0))
    visits = {(0, 0)}
    for line in open(fn):
        for ch in line:
            x, y = pos[0]
            x, y = update(x, y, ch)
            visits.add((x, y))
            pos = (pos[1], (x, y))
        print(len(visits))
