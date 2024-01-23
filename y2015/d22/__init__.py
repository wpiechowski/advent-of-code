import dataclasses
import heapq
from dataclasses import dataclass


@dataclass
class State:
    p_hit: int
    mana: int
    boss_hit: int
    boss_damage: int
    armor: int = 0
    shield_timer: int = 0
    poison_timer: int = 0
    recharge_timer: int = 0
    spent: int = 0
    history: str = ""

    def astuple(self):
        return (
            self.p_hit,
            self.mana,
            self.boss_hit,
            self.boss_damage,
            self.shield_timer,
            self.poison_timer,
            self.recharge_timer,
        )

    def __eq__(self, other):
        return self.spent == other.spent

    def __lt__(self, other):
        return self.spent < other.spent


def process_spells(s: State, pr: bool = False):
    if s.poison_timer:
        s.poison_timer -= 1
        s.boss_hit -= 3
        if pr:
            print(f"Poison deals 3 damage; its timer is now {s.poison_timer}")
    if s.shield_timer:
        s.shield_timer -= 1
        s.armor = 7
        if pr:
            print(f"Shield's timer is now {s.shield_timer}")
    else:
        s.armor = 0
    if s.recharge_timer:
        s.recharge_timer -= 1
        s.mana += 101
        if pr:
            print(f"Recharge provides 101 mana; its timer is now {s.recharge_timer}")
    return s


def turn(s: State, force: str = "") -> list[State]:
    # player:
    if force:
        print("-- Player turn --")
        print(f"- Player has {s.p_hit} hit points, {s.armor} armor, {s.mana} mana")
        print(f"- Boss has {s.boss_hit} hit points")
    # part 2
    s.p_hit -= 1
    if s.p_hit <= 0:
        return [s]
    process_spells(s, bool(force))
    states = []
    # missile:
    if s.mana >= 53 and force in ("m", ""):
        s2 = dataclasses.replace(s)
        s2.mana -= 53
        s2.spent += 53
        s2.boss_hit -= 4
        s2.history += "m"
        states.append(s2)
        if force:
            print(f"Player casts Magic Missile, dealing 4 damage.")
    # drain
    if s.mana >= 73 and force in ("d", ""):
        s2 = dataclasses.replace(s)
        s2.mana -= 73
        s2.spent += 73
        s2.boss_hit -= 2
        s2.p_hit += 2
        s2.history += "d"
        states.append(s2)
        if force:
            print("Player casts Drain, dealing 2 damage, and healing 2 hit points.")
    # shield
    if s.mana >= 113 and s.shield_timer == 0 and force in ("s", ""):
        s2 = dataclasses.replace(s)
        s2.mana -= 113
        s2.spent += 113
        s2.shield_timer = 6
        s2.history += "s"
        s2.armor = 7
        states.append(s2)
        if force:
            print("Player casts Shield, increasing armor by 7.")
    # poison
    if s.mana >= 173 and s.poison_timer == 0 and force in ("p", ""):
        s2 = dataclasses.replace(s)
        s2.mana -= 173
        s2.spent += 173
        s2.poison_timer = 6
        s2.history += "p"
        states.append(s2)
        if force:
            print("Player casts Poison.")
    # recharge
    if s.mana >= 229 and s.recharge_timer == 0 and force in ("r", ""):
        s2 = dataclasses.replace(s)
        s2.mana -= 229
        s2.spent += 229
        s2.recharge_timer = 5
        s2.history += "r"
        states.append(s2)
        if force:
            print("Player casts Recharge.")
    if force:
        print("")
    # boss turn
    ret = []
    for s in states:
        if force:
            print("-- Boss turn --")
            print(f"- Player has {s.p_hit} hit points, {s.armor} armor, {s.mana} mana")
            print(f"- Boss has {s.boss_hit} hit points")
        process_spells(s, bool(force))
        attack = max(1, s.boss_damage - s.armor)
        if force:
            print(f"Boss attacks for {attack} damage!")
        s.p_hit -= attack
        ret.append(s)
    if force:
        print("")
    return ret


def replay(s: State, moves: str):
    for m in moves:
        ss = turn(s, m)
        if len(ss) != 1:
            print(ss)
            return
        s = ss[0]
    return s


def task1():
    s0 = State(50, 500, 58, 9)
    # s0 = State(10, 250, 14, 8)
    cache = set()
    cache_hits = 0
    q = [s0]
    best = None
    while q:
        s = heapq.heappop(q)
        # print(s)
        t = s.astuple()
        if t in cache:
            cache_hits += 1
            continue
        cache.add(t)
        ss = turn(s)
        for s2 in ss:
            if s2.boss_hit <= 0:
                # win
                print(s2.spent, s2.history, cache_hits)
                print(s2)
                if best is None or s2.spent < best.spent:
                    best = s2
                # continue
                # replay(s0, s2.history)
                return
            if s2.p_hit <= 0:
                # lost
                continue
            st = s2.astuple()
            if st in cache:
                continue
            heapq.heappush(q, s2)
    print(best)


def task1_():
    s0 = State(50, 500, 58, 9)
    txt = "prsprdpmm"
    s = replay(s0, txt)
    print(s)
