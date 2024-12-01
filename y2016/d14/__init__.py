from hashlib import md5
import re
from functools import cache


re_5 = re.compile("(" + "|".join([x*5 for x in "0123456789abcdef"]) + ")")
re_3 = re.compile("(" + "|".join([x*3 for x in "0123456789abcdef"]) + ")")


@cache
def get_hash(pos: int) -> str:
    # salt = "abc"
    salt = "qzyelonm"
    txt = salt + str(pos)
    for _ in range(2017):
        d = txt.encode("ascii")
        m = md5(d)
        d = m.digest()
        txt = d.hex()
    return txt


def task1():
    results = []
    pos = 0
    vals = []
    while len(results) < 64:
        d = get_hash(pos)
        print(len(results), pos, d)
        if m3 := re_3.search(d):
            for p2 in range(pos + 1, pos + 1001):
                d2 = get_hash(p2)
                if m3[1][0] * 5 in d2:
                    results.append(pos)
                    # print(pos)
                    break
        pos += 1
    print(results[-1])
