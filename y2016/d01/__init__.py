from tools import get_lines


def task1():
    x, y = 0, 0
    dx, dy = 0, 1
    fn = "i.txt"
    for line in get_lines(fn):
        for cmd in line.split(", "):
            if cmd[0] == "L":
                dx, dy = -dy, dx
            else:
                dx, dy = dy, -dx
            d = int(cmd[1:])
            x += d * dx
            y += d * dy
    print(abs(x) + abs(y))


def task2():
    import pylab as plt
    x, y = 0, 0
    dx, dy = 0, 1
    visited = {x, y}
    fn = "i.txt"
    for line in get_lines(fn):
        for cmd in line.split(", "):
            print(x, y, cmd)
            if cmd[0] == "L":
                dx, dy = -dy, dx
            else:
                dx, dy = dy, -dx
            d = int(cmd[1:])
            for _ in range(d):
                x += dx
                y += dy
                if (x, y) in visited:
                    print(abs(x) + abs(y))
                    return
                visited.add((x, y))
