from hashlib import md5
from collections import Counter, deque

salt = "lpvhkcbi"
end = 3, 3


def iter_open(path: str) -> str:
    cnt = Counter(path)
    pos_x = cnt["R"] - cnt["L"]
    pos_y = cnt["D"] - cnt["U"]
    if (pos_x, pos_y) == end:
        yield path + "."
        return
    if pos_x < 0 or pos_x > end[0]:
        return
    if pos_y < 0 or pos_y > end[1]:
        return
    text = salt + path
    h = md5(text.encode("ascii"))
    digest = h.digest().hex()
    for digit, dir in zip(digest, "UDLR"):
        if digit in "bcdef":
            yield path + dir


def task1():
    path = ""
    q = deque([path])
    while q:
        cur = q.popleft()
        for path in iter_open(cur):
            if path[-1] == ".":
                print(len(q), len(path) - 1, path[:-1])
            else:
                q.append(path)
