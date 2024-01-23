def task1():
    fn = "y2015/d01/i.txt"
    for line in open(fn):
        print(line)
        here = 0
        for ch in line:
            here += 1 if ch == "(" else -1
        print(here)


def task2():
    fn = "y2015/d01/i.txt"
    for line in open(fn):
        print(line)
        here = 0
        pos = 0
        for ch in line:
            here += 1 if ch == "(" else -1
            pos += 1
            if here == -1:
                print(pos)
                break
