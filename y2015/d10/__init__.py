def change(txt: str) -> str:
    out = ""
    k = 0
    while k < len(txt):
        ch = txt[k]
        for n in range(k, len(txt)):
            if txt[n] != ch:
                n -= 1
                break
        out += str(n + 1 - k) + ch
        k = n + 1
    return out


def task1():
    txt = "1113122113"
    for i in range(50):
        txt = change(txt)
        print(i, len(txt))
    print(len(txt))
