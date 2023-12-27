import re


re_game = re.compile(r"Game (\d+): (.*)")


def test_game(line: str):
    intro = re_game.match(line)
    if not intro:
        return 0, (0, 0, 0)
    draws = intro.group(2).split("; ")
    maxes = [0, 0, 0]
    for draw in draws:
        for color in draw.split(", "):
            vals = color.split(" ")
            count, name = vals
            count = int(count)
            if name == "red":
                index = 0
            elif name == "green":
                index = 1
            else:
                index = 2
            if count > maxes[index]:
                maxes[index] = count
    return int(intro.group(1)), maxes


def task1():
    limits = (12, 13, 14)
    ret = 0
    for line in open("i02a.txt"):
        game, vals = test_game(line.strip())
        for l, v in zip(limits, vals):
            if v > l:
                break
        else:
            ret += game
    print(ret)


def task2():
    ret = 0
    for line in open("i02a.txt"):
        game, vals = test_game(line.strip())
        pwr = vals[0] * vals[1] * vals[2]
        ret += pwr
    print(ret)
