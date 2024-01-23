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
        "J": 1,
        "Q": 12,
        "K": 13,
        "A": 14,
    }

    subs = "23456789TQKA"

    def __init__(self, cards: str, bid: int):
        self.hand_str = cards
        self.hand_vals = tuple(map(lambda x: self.card_vals[x], cards))
        self.bid = int(bid)
        self.key = (self.calc_key(self.hand_str),) + self.hand_vals

    def __str__(self):
        return self.hand_str

    def iter_j_hands(self, hand_str: str, min_ndx: int):
        if not hand_str:
            yield ""
            return
        if hand_str[0] != "J":
            for h in self.iter_j_hands(hand_str[1:], min_ndx):
                yield hand_str[0] + h
        else:
            for n in range(min_ndx, len(self.subs)):
                for h in self.iter_j_hands(hand_str[1:], n):
                    yield self.subs[n] + h

    def calc_key(self, hand_str: str):
        best = -7
        for h in self.iter_j_hands(hand_str, 0):
            k = self.calc_key_single(h)
            best = max(best, k)
            # print(h, k)
        return best

    def calc_key_single(self, hand_str: str):
        sc = sorted(hand_str)
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


def task2():
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
