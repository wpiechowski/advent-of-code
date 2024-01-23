import re

re_thing = re.compile(r"([0-9]+)|([^0-9.])")


def scan_line(line: str):
    syms = []   # (pos, code)
    nums = []   # (val, pos0, pos1)
    x = 0
    while True:
        m = re_thing.search(line, x)
        if not m:
            break
        if m[1]:
            nums.append((
                int(m[0]), m.start(0), m.end(0),
            ))
        else:
            syms.append((m.start(0), m[2]))
        x = m.end(0)
    return syms, nums


def check_lines(syms, nums):
    ret = 0
    for sx in syms:
        for val, x0, x1 in nums:
            if x0 - 1 <= sx <= x1:
                ret += val
    return ret


def check_lines2(syms, nums0, nums1, nums2):
    ret = 0
    for sx, code in syms:
        vals = []
        if code != "*":
            continue
        for nums in (nums0, nums1, nums2):
            for val, x0, x1 in nums:
                if x0 - 1 <= sx <= x1:
                    vals.append(val)
        if len(vals) == 2:
            ret += vals[0] * vals[1]
    return ret


def wio(syms, nums):
    ret = 0
    for line_num, line_syms in enumerate(syms):
        if line_num > 0:
            nums0 = nums[line_num - 1]
        else:
            nums0 = []
        if line_num < len(nums) - 1:
            nums2 = nums[line_num + 1]
        else:
            nums2 = []
        ret += check_lines2(line_syms, nums0, nums[line_num], nums2)
    return ret


def task1():
    syms = []
    nums = []
    for line in open("i03a.txt"):
        s, n = scan_line(line.strip())
        print(line.strip(), s, n)
        syms.append(s)
        nums.append(n)
    ret = wio(syms, nums)
    print(ret)
