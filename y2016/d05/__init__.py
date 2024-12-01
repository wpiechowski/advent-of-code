import hashlib


def task1():
    # seed = "abc"
    seed = "wtnhxymk"
    key = ""
    for n in range(100000000):
        txt = seed + str(n)
        h = hashlib.md5(txt.encode("ascii"))
        d = h.digest().hex()
        if d[:5] == "00000":
            print(txt, d)
            key += d[5]
            if len(key) == 8:
                break
    print(key)


def task2():
    # seed = "abc"
    seed = "wtnhxymk"
    pwd = "________"
    to_go = len(pwd)
    key = ""
    for n in range(100000000):
        txt = seed + str(n)
        h = hashlib.md5(txt.encode("ascii"))
        d = h.digest().hex()
        if d[:5] == "00000":
            print(txt, d)
            if d[5] not in "01234567":
                continue
            pos = int(d[5])
            if pwd[pos] != "_":
                continue
            pwd = pwd[:pos] + d[6] + pwd[pos + 1:]
            print(pwd)
            to_go -= 1
            if not to_go:
                break
    print(key)
