import re
from dataclasses import dataclass

from tools import get_lines

fn = "i.txt"
re_init = re.compile(r"value (\d+) goes to bot (\d+)")
re_pass = re.compile(r"bot (\d+) gives low to (bot|output) (\d+) and high to (bot|output) (\d+)")


@dataclass
class Bot:
    id: int
    low: int = 0
    high: int = 0
    chips: list[int] = None


def load():
    bots: dict[int, Bot] = {}
    signs = {
        "bot": 0,
        "output": 1000,
    }
    for line in get_lines(fn):
        if m := re_init.match(line):
            i = int(m[2])
            if i not in bots:
                b = Bot(id=i, chips=[])
                bots[i] = b
            bots[i].chips.append(int(m[1]))
        elif m := re_pass.match(line):
            i = int(m[1])
            low = int(m[3]) + signs[m[2]]
            high = int(m[5]) + signs[m[4]]
            for num in (i, low, high):
                if num not in bots:
                    b = Bot(id=num, chips=[])
                    bots[num] = b
            bots[i].high = high
            bots[i].low = low
        else:
            ic(line)
    return bots


def find_active(bots: dict[int, Bot]) -> Bot:
    for bot in bots.values():
        if len(bot.chips) >= 2:
            return bot


def task1():
    checkpoint = (17, 61)
    bots = load()
    ic(bots)
    while bot := find_active(bots):
        low = min(bot.chips)
        high = max(bot.chips)
        if (low, high) == checkpoint:
            ic(bot.id)
        ic(bot.id, bot.chips, bot.low, bot.high)
        bots[bot.low].chips.append(low)
        bots[bot.high].chips.append(high)
        bot.chips = []
    ic(bots[1000])
    ic(bots[1001])
    ic(bots[1002])
