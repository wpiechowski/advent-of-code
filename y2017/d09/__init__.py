from tools import *


re_cancel = re.compile(r"!.")
re_garbage = re.compile(r"<.*?>|,")
re_garbage2 = re.compile(r"<.*?>")


def clean(txt: str) -> str:
    txt = re_cancel.sub("", txt)
    txt = re_garbage.sub("", txt)
    return txt


def count(txt: str) -> int:
    nest = 0
    score = 0
    for ch in txt:
        if ch == "{":
            nest += 1
            score += nest
        else:
            nest -= 1
    return score


def task1():
    for line in get_lines("i.txt"):
        line = clean(line)
        ic(count(line))


def clean2(txt: str) -> int:
    txt, cancels = re_cancel.subn("", txt)
    l1 = len(txt)
    txt, garbage = re_garbage2.subn("", txt)
    cnt = l1 - len(txt) - 2 * garbage
    return cnt


def task2():
    for line in get_lines("i.txt"):
        cl = clean2(line)
        ic(cl)
