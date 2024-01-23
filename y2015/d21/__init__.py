from dataclasses import dataclass


@dataclass
class Player:
    hit: int
    damage: int
    armor: int


weapons = [
    (8, 4),
    (10, 5),
    (25, 6),
    (40, 7),
    (74, 8),
]

armors = [
    (0, 0),
    (13, 1),
    (31, 2),
    (53, 3),
    (75, 4),
    (102, 5),
]

rings = [
    (0, 0, 0),
    (0, 0, 0),
    (25, 1, 0),
    (50, 2, 0),
    (100, 3, 0),
    (20, 0, 1),
    (40, 0, 2),
    (80, 0, 3),
]


def fight(p1: Player, p2: Player) -> bool:
    d1_2 = max(1, p1.damage - p2.armor)
    d2_1 = max(1, p2.damage - p1.armor)
    p1_t = p1.hit // d2_1
    p2_t = p2.hit // d1_2
    return p1_t >= p2_t


def task1():
    p2 = Player(100, 8, 2)
    best_cost = 1000
    for weapon in weapons:
        for armor in armors:
            for nr, ring1 in enumerate(rings):
                for ring2 in rings[nr + 1:]:
                    cost = weapon[0] + armor[0] + ring1[0] + ring2[0]
                    p1 = Player(100, weapon[1] + ring1[1] + ring2[1], armor[1] + ring1[2] + ring2[2])
                    print(cost, p1)
                    win = fight(p1, p2)
                    if win:
                        best_cost = min(cost, best_cost)
    print(best_cost)


def task2():
    p2 = Player(100, 8, 2)
    best_cost = 0
    for weapon in weapons:
        for armor in armors:
            for nr, ring1 in enumerate(rings):
                for ring2 in rings[nr + 1:]:
                    cost = weapon[0] + armor[0] + ring1[0] + ring2[0]
                    p1 = Player(100, weapon[1] + ring1[1] + ring2[1], armor[1] + ring1[2] + ring2[2])
                    print(cost, p1)
                    win = fight(p1, p2)
                    if not win:
                        best_cost = max(cost, best_cost)
    print(best_cost)
