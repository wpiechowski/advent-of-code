from tools import *


def task1():
    lines = list(get_lines("i.txt", strip=False))

    def get(y, x):
        if x < 0 or y < 0:
            return " "
        if y >= len(lines) or x >= len(lines[y]):
            return " "
        else:
            ret = lines[y][x]
            if ret == "\n":
                ret = " "
            return ret

    y = 0
    x = 0
    for x, c in enumerate(lines[0]):
        if c != " ":
            break
    dy = 1
    dx = 0
    ret = ""
    steps = 0
    while x >= 0:
        c = get(y, x)
        if c == " ":
            break
        if c.isalpha():
            ret += c
        if c == "+":
            ic(ret, y, x, c)
            for cx, cy, _ in directions:
                if cx == -dx and cy == -dy:
                    continue
                if cx == dx and cy == dy:
                    continue
                if cc := get(y + cy, x + cx) != " ":
                    if cx == 0 and cc == "-":
                        continue
                    if cy == 0 and cc == "|":
                        continue
                    ic(dx, dy, cx, cy, c)
                    dx = cx
                    dy = cy
                    break
            else:
                break
        x += dx
        y += dy
        steps += 1
    ic(ret, steps)
