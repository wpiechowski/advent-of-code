from tools import get_re_lines

re_line = r" *(\d+) +(\d+) +(\d+)"
fn = "i.txt"


def task1():
    ok = 0
    for m in get_re_lines(fn, re_line):
        vals = list(map(int, m))
        vals.sort()
        if vals[0] + vals[1] > vals[2]:
            ok += 1
    print(ok)


def task2():
    ok = 0
    buf = []
    for m in get_re_lines(fn, re_line):
        vals = list(map(int, m))
        buf.append(vals)
        if len(buf) == 3:
            for x in range(3):
                vals = [buf[0][x], buf[1][x], buf[2][x]]
                vals.sort()
                if vals[0] + vals[1] > vals[2]:
                    ok += 1
            buf = []
    print(ok)
