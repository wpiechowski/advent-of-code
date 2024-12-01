def step(a: str) -> str:
    b = a[::-1].replace("0", "o").replace("1", "0").replace("o", "1")
    return a + "0" + b


def cksum(x: str) -> str:
    while True:
        c = ""
        for n in range(0, len(x) - 1, 2):
            if x[n] == x[n + 1]:
                c += "1"
            else:
                c += "0"
        x = c
        if len(x) & 1 == 1:
            return x


def task1():
    p = "00111101111101000"
    max_len = 35651584  # 272
    while len(p) < max_len:
        p = step(p)
        print(len(p))
    p = p[:max_len]
    ic(cksum(p))
