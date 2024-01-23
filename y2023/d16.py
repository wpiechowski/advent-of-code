class Beam:
    def __init__(self, pos: tuple[int, int], heading: tuple[int, int]):
        self.pos = pos
        self.heading = heading

    def __repr__(self):
        return f"Beam({self.pos}, {self.heading})"


class Cell:
    def __init__(self, contents: str):
        self.contents = contents
        self.beams_in = set()

    def reset(self):
        self.beams_in = set()

    def beam_in(self, b: Beam) -> list[Beam]:
        if b.heading in self.beams_in:
            return []
        self.beams_in.add(b.heading)
        ret = []
        if self.contents == ".":
            b.pos = b.pos[0] + b.heading[0], b.pos[1] + b.heading[1]
            ret = [b]
        elif self.contents == "/":
            b.pos = b.pos[0] - b.heading[1], b.pos[1] - b.heading[0]
            b.heading = -b.heading[1], -b.heading[0]
            ret = [b]
        elif self.contents == "\\":
            b.pos = b.pos[0] + b.heading[1], b.pos[1] + b.heading[0]
            b.heading = b.heading[1], b.heading[0]
            ret = [b]
        elif self.contents == "|":
            if b.heading[0] == 0:
                b.pos = b.pos[0] + b.heading[0], b.pos[1] + b.heading[1]
                ret = [b]
            else:
                ret = [
                    Beam((b.pos[0], b.pos[1] - 1), (0, -1)),
                    Beam((b.pos[0], b.pos[1] + 1), (0, 1)),
                ]
        elif self.contents == "-":
            if b.heading[1] == 0:
                b.pos = b.pos[0] + b.heading[0], b.pos[1] + b.heading[1]
                ret = [b]
            else:
                ret = [
                    Beam((b.pos[0] - 1, b.pos[1]), (-1, 0)),
                    Beam((b.pos[0] + 1, b.pos[1]), (1, 0)),
                ]
        else:
            raise ValueError("WTF")
        return ret

    def __str__(self):
        return "*" if self.beams_in else self.contents


def load_maze(f):
    lines = []
    for y, line in enumerate(f):
        line = line.strip()
        lines.append([])
        for x, ch in enumerate(line):
            c = Cell(ch)
            lines[-1].append(c)
    return lines


def energize(maze: list[list[Cell]], beams: list[Beam]):
    while beams:
        b = beams.pop()
        if 0 <= b.pos[0] < len(maze[0]) and \
            0 <= b.pos[1] < len(maze):
            bb = maze[b.pos[1]][b.pos[0]].beam_in(b)
            beams.extend(bb)
            # print_maze(maze, beams)
            # print(beams)


def calc_energized(maze: list[list[Cell]]) -> int:
    ret = 0
    for line in maze:
        for c in line:
            if c.beams_in:
                ret += 1
    return ret


def print_maze(maze: list[list[Cell]], beams):
    print(beams)
    for line in maze:
        print("".join(map(str, line)))


def task1():
    fn = "i16a.txt"
    maze = load_maze(open(fn))
    beams = [Beam((0, 0), (1, 0))]
    energize(maze, beams)
    ret = calc_energized(maze)
    print(ret)


def reset_maze(maze: list[list[Cell]]):
    for line in maze:
        for c in line:
            c.reset()


def task2():
    fn = "i16a.txt"
    best = 0
    maze = load_maze(open(fn))
    lx = len(maze[0])
    ly = len(maze)
    start_beams = []
    for x in range(lx):
        start_beams.append(Beam((x, 0), (0, 1)))
        start_beams.append(Beam((x, ly - 1), (0, -1)))
    for y in range(ly):
        start_beams.append(Beam((0, y), (1, 0)))
        start_beams.append(Beam((lx - 1, y), (-1, 0)))
    for b in start_beams:
        reset_maze(maze)
        energize(maze, [b])
        e = calc_energized(maze)
        print(b, e)
        best = max(e, best)
    print(best)
