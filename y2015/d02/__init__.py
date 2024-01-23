def task1():
    fn = "y2015/d02/i.txt"
    ret = 0
    for line in open(fn):
        x, y, z = tuple(map(int, line.split("x")))
        s = min(x*y, x*z, y*z)
        a = s + 2 * (x * y + x * z + y * z)
        ret += a
    print(ret)


def task2():
    fn = "y2015/d02/i.txt"
    ret = 0
    for line in open(fn):
        vals = sorted(tuple(map(int, line.split("x"))))
        vol = vals[0] * vals[1] * vals[2]
        ret += 2 * (vals[0] + vals[1]) + vol
    print(ret)
