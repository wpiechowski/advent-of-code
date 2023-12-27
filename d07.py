from operator import attrgetter


class Hand:
    card_vals = {
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "T": 10,
        "J": 11,
        "Q": 12,
        "K": 13,
        "A": 14,
    }

    def __init__(self, cards: str, bid: int):
        self.hand_str = cards
        self.hand_vals = tuple(map(lambda x: self.card_vals[x], cards))
        self.bid = int(bid)
        self.key = (self.calc_key(),) + self.hand_vals

    def __str__(self):
        return self.hand_str

    def calc_key(self):
        sc = sorted(self.hand_str)
        cc = [(1, sc[0])]
        for c in sc[1:]:
            if c != cc[-1][1]:
                cc.append((1, c))
            else:
                cc[-1] = (cc[-1][0] + 1, c)
        cc.sort(reverse=True)
        if cc[0][0] == 5:
            return -1
        if cc[0][0] == 4:
            return -2
        if cc[0][0] == 3 and cc[1][0] == 2:
            return -3
        if cc[0][0] == 3:
            return -4
        if cc[0][0] == 2 and cc[1][0] == 2:
            return -5
        if cc[0][0] == 2:
            return -6
        return -7


def task1():
    hands = []
    for line in open("i07a.txt"):
        cards, bid = line.strip().split(" ")
        h = Hand(cards, bid)
        hands.append(h)
    hands.sort(key=attrgetter("key"), reverse=False)
    val = 0
    for m, h in enumerate(hands):
        print(h, h.key)
        val += (m + 1) * h.bid
    print(val)
