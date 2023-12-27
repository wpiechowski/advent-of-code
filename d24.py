import numpy as np
from scipy.optimize import fsolve


def load(fn: str):
    ret = []
    for line in open(fn):
        pos, vel = line.strip().split(" @ ")
        pos = tuple(map(int, pos.split(", ")))
        vel = tuple(map(int, vel.split(", ")))
        ret.append((pos, vel))
    return ret


def find_xy_crossing(b1, b2):
    p10 = complex(b1[0][0], b1[0][1])
    v10 = complex(b1[1][0], b1[1][1])
    p20 = complex(b2[0][0], b2[0][1])
    v20 = complex(b2[1][0], b2[1][1])
    p1 = p10 - p20
    p1 /= v20
    v1 = v10 / v20
    if v1.imag == 0:
        return None, None, None
    p2t = p1.real - p1.imag * v1.real / v1.imag
    p1t = (complex(p2t, 0) - p1) / v1
    m1 = p10 + v10 * p1t
    # m2 = p20 + v20 * p2t
    return p1t.real, p2t, m1


def task1():
    fn = "i24a.txt"
    balls = load(fn)
    # print(balls)
    found = 0
    bounds = (200000000000000, 400000000000000)
    for b1 in balls:
        for b2 in balls:
            if b1 == b2:
                break
            print(b1, b2)
            p1t, p2t, m1 = find_xy_crossing(b1, b2)
            print(p1t, p2t, m1)
            if p1t is None:
                continue
            if p1t < 0 or p2t < 0:
                continue
            if (bounds[0] <= m1.real <= bounds[1]) and (bounds[0] <= m1.imag <= bounds[1]):
                found += 1
    print(found)


def task2():
    fn = "i24a.txt"
    balls = load(fn)

    def optfunc(vars):
        b0 = 5
        (p0x, p0y, p0z, v0x, v0y, v0z) = vars
        ret = []
        for ball in balls[b0:b0+3]:
            (p1x, p1y, p1z), (v1x, v1y, v1z) = ball
            ret.append((p0x - p1x) * (v1y - v0y) - (p0y - p1y) * (v1x - v0x))
            ret.append((p0x - p1x) * (v1z - v0z) - (p0z - p1z) * (v1x - v0x))
        return ret

    x0 = np.array(balls[0][0] + balls[0][1], float)
    print(x0)
    res = fsolve(optfunc, x0)
    list(map(print, res))
    print(sum(res[:3]))
    o = optfunc(res)
    print(o)

"""
pos1 + vel1 * t1 = pos0 + vel0 * t1
pos2 + vel2 * t2 = pos0 + vel0 * t2

vars:
pos (3), vel (3), t (n)
eqs:
3*n

p1x + v1x*t1 = p0x + v0x*t1
p1y + v1y*t1 = p0y + v0y*t1
p1z + v1z*t1 = p0z + v0z*t1

t1(v1x-v0x) = p0x - p1x
t1 = (p0x - p1x) / (v1x - v0x)

(p0x - p1x) * (v1y - v0y) = (p0y - p1y) * (v1x - v0x)
  
p2x + v2x*t2 = p0x + v0x*t2
p2y + v2y*t2 = p0y + v0y*t2
p2z + v2z*t2 = p0z + v0z*t2

p3x + v3x*t3 = p0x + v0x*t3
p3y + v3y*t3 = p0y + v0y*t3
p3z + v3z*t3 = p0z + v0z*t3


(p1x + p1y + p1z) + t1 * (v1x + v1y + v1z) = (p0x + p0y + p0z) + t1 * (v0x + v0y + v0z)

Sp1 + t1 * Sv1 = Sp0 + t1 * Sv0


t1*(v1x-v0x) + (p1x - p0x) = 0


vars: tn p0x p0y p0z tn*
"""


def task2_():
    fn = "i24a.txt"
    balls = load(fn)
