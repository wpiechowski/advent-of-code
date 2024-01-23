from tools import get_lines

fn = "i.txt"
dirs = {
    "L": (-1, 0),
    "R": (1, 0),
    "U": (0, -1),
    "D": (0, 1),
}


def task1():
    keys = ["123", "456", "789"]
    x, y = 1, 1
    for line in get_lines(fn):
        for ch in line:
            dx, dy = dirs[ch]
            x, y = x + dx, y + dy
            x = min(2, max(0, x))
            y = min(2, max(0, y))
        print(keys[y][x])


def task2():
    keys = [
        "       ",
        "  234  ",
        " 56789 ",
        "  ABC  ",
        "   D   ",
        "       ",
    ]
    x, y = 1, 2
    for line in get_lines(fn):
        for ch in line:
            dx, dy = dirs[ch]
            x2, y2 = x + dx, y + dy
            if keys[y2][x2] != " ":
                x, y = x2, y2
        print(keys[y][x])
