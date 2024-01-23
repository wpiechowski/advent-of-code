from functools import reduce


def factors(n):
    return set(reduce(list.__add__,
                ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))


def task1():
    target = 29000000 // 10
    for k in range(1, 1000000):
        f = factors(k)
        s = sum(f)
        print(k, s)
        if s >= target:
            break


def task2():
    target = 29000000 / 11
    for k in range(1, 10000000):
        f = factors(k)
        ff = filter(lambda x: k <= x * 50, f)
        s = sum(ff)
        print(k, s)
        if s >= target:
            break
