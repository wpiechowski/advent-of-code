import re
import json


re_num = re.compile(r"(-?\d+)")


def task1():
    vals = 0
    for line in open("y2015/d12/i.txt"):
        for m in re_num.finditer(line):
            vals += int(m[1])
    print(vals)


def calc_sum(obj) -> int:
    if type(obj) is int:
        return obj
    if type(obj) is str:
        return 0
    if type(obj) is dict:
        tmp_sum = 0
        for k, v in obj.items():
            tmp_sum += calc_sum(v)
            if v == "red":
                tmp_sum = 0
                break
        return tmp_sum
    if type(obj) is list:
        tmp_sum = 0
        for item in obj:
            tmp_sum += calc_sum(item)
        return tmp_sum


def task2():
    fn = "y2015/d12/i.txt"
    j = json.load(open(fn))
    print(calc_sum(j))
