def is_nice(t: str):
    vowels = 0
    double = 0
    prev = "-"
    for ch in t:
        d = prev + ch
        if ch in "aeoiu":
            vowels += 1
        if ch == prev:
            double += 1
        if d in ("ab", "cd", "pq", "xy"):
            return False
        prev = ch
    return vowels >= 3 and double >= 1


def is_nice2(t: str):
    found = False
    for i2 in range(2, len(t) - 1):
        for i1 in range(i2 - 1):
            if t[i1:i1 + 2] == t[i2:i2 + 2]:
                found = True
                break
        if found:
            break
    if not found:
        return False
    for i in range(len(t) - 2):
        if t[i] == t[i + 2]:
            return True
    return False


def task1():
    fn = "y2015/d05/i.txt"
    nice = 0
    for line in open(fn):
        line = line.strip()
        n = is_nice2(line)
        print(line, n)
        nice += n
    print(nice)
