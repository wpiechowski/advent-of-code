allowed = "abcdefghjkmnpqrstuvwxyz"
all_chars = "abcdefghijklmnopqrstuvwxyz"


triples = [all_chars[i:i+3] for i in range(len(all_chars) - 2)]


def check(pwd: str) -> bool:
    for ch in pwd:
        if ch not in allowed:
            return False
    dbl = ""
    ok = False
    for c1, c2 in zip(pwd[1:], pwd[:-1]):
        if c1 == c2:
            if dbl and c1 != dbl:
                ok = True
                break
            else:
                dbl = c1
    if not ok:
        return False
    ok = False
    for i in range(len(pwd) - 2):
        if pwd[i:i+3] in triples:
            ok = True
            break
    return ok


def next_char(ch: str):
    pos = all_chars.find(ch)
    if pos == len(all_chars) - 1:
        return "-a"
    pos += 1
    while all_chars[pos] not in allowed:
        pos += 1
    return all_chars[pos]


def next_pwd(pwd: str) -> str:
    i = len(pwd) - 1
    while True:
        ch = next_char(pwd[i])
        if ch != "-a":
            pwd = pwd[:i] + ch + pwd[i+1:]
            break
        else:
            pwd = pwd[:i] + "a" * (len(pwd) - i)
            i -= 1
    return pwd


def task1():
    pwd = "vzbxxyzz"
    # print(check("ghjaabcc"))
    while True:
        pwd = next_pwd(pwd)
        print(pwd)
        if check(pwd):
            break


