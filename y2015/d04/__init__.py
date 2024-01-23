from hashlib import md5


def task1():
    key = b"yzbqklnj"
    for i in range(1, 1000000000):
        m = md5()
        k = key + str(i).encode("ascii")
        m.update(k)
        h = m.digest()
        if h[:2] == b"\x00\x00" and (h[2] & 0xff == 0):
            print(i, k, h)
            return
        i += 1
