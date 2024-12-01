from tools import get_lines

fn = "i.txt"


def is_abba(s: str) -> bool:
    for n in range(len(s) - 3):
        if s[n] == s[n + 1]:
            continue
        if s[n] == s[n + 3] and s[n + 1] == s[n + 2]:
            return True
    return False


def split_line(s: str):
    s = s.replace("]", "[")
    return s.split("[")


def task1():
    cnt = 0
    for line in get_lines(fn):
        strs = split_line(line)
        ab = list(map(is_abba, strs))
        if any(ab[::2]) and not any(ab[1::2]):
            cnt += 1
            print(cnt, line, ab)


def iter_aba(s: str):
    for n in range(len(s) - 2):
        if s[n] == s[n + 1]:
            continue
        if s[n] == s[n + 2]:
            yield s[n: n + 3], s[n + 1: n + 3] + s[n + 1]


def task2():
    cnt = 0
    for line in get_lines(fn):
        strs = split_line(line)
        for h in strs[::2]:
            for aba, bab in iter_aba(h):
                for h2 in strs[1::2]:
                    if bab in h2:
                        cnt += 1
                        print(cnt, aba, strs)
                        break
                else:
                    continue
                break
            else:
                continue
            break
