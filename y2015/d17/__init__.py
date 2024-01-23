from tools import get_path, get_lines

fn = "i.txt"


def task1():
    target = 150
    lines = list(map(int, get_lines(get_path() + fn)))
    print(len(lines), lines)
    good = 0
    least = len(lines)
    for n in range(2**len(lines)):
        vol_sum = 0
        bit_cnt = 0
        for bit, vol in enumerate(lines):
            if n & (1<<bit):
                vol_sum += vol
                bit_cnt += 1
        if vol_sum == target:
            print(n, bit_cnt)
            if bit_cnt < least:
                least = bit_cnt
                good = 0
            if bit_cnt == least:
                good += 1
    print("count", good)
