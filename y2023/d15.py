def iter_steps(f):
    for line in f:
        for s in line.strip().split(","):
            yield s


def calc_hash(s: str) -> int:
    h = 0
    for ch in s:
        h = ((h + ord(ch)) * 17) & 255
    return h


def task1():
    fn = "i15a.txt"
    sh = 0
    for s in iter_steps(open(fn)):
        sh += calc_hash(s)
    print(sh)


def process_lens(boxes: list[list[tuple[str, int]]], oper: str):
    if oper[-1] == "-":
        name = oper[:-1]
    else:
        name, val = oper.split("=")
        val = int(val)
    box_n = calc_hash(name)
    found = False
    lens_n = -1
    for lens_n, (n, _) in enumerate(boxes[box_n]):
        if n == name:
            found = True
            break
    if oper[-1] == "-":
        if found:
            boxes[box_n].pop(lens_n)
    else:
        if found:
            boxes[box_n][lens_n] = (name, val)
        else:
            boxes[box_n].append((name, val))


def calc_score(boxes: list[list[tuple[str, int]]]):
    ret = 0
    for box_n, box in enumerate(boxes):
        for lens_n, (_, val) in enumerate(box):
            ret += (box_n + 1) * (lens_n + 1) * val
    return ret


def print_boxes(boxes: list[list[tuple[str, int]]]):
    for box_n, box in enumerate(boxes):
        if not box:
            continue
        text = f"Box {box_n}: "
        text += " ".join(map(lambda x: f"[{x[0]} {x[1]}]", box))
        print(text)


def task2():
    fn = "i15a.txt"
    boxes = []
    for _ in range(256):
        boxes.append([])
    for s in iter_steps(open(fn)):
        process_lens(boxes, s)
    print_boxes(boxes)
    r = calc_score(boxes)
    print(r)
