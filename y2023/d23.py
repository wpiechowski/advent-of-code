import numpy as np
import time


CELL_EMPTY = 0
CELL_WALL = 1
CELL_UP = 2
CELL_RIGHT = 3
CELL_DOWN = 4
CELL_LEFT = 5


def load(fn: str):
    ret = []
    vals = {
        ".": CELL_EMPTY,
        "#": CELL_WALL,
        ">": CELL_RIGHT,
        "<": CELL_LEFT,
        "^": CELL_UP,
        "v": CELL_DOWN,
    }
    for line in open(fn):
        ret.append([])
        for ch in line.strip():
            ret[-1].append(vals[ch])
    return np.array(ret)


class Path:
    def __init__(self):
        self.points: list[tuple[int, int]] = []
        self.length = 0

    def clone(self):
        p2 = Path()
        p2.points = self.points.copy()
        p2.length = self.length
        return p2

    def __repr__(self):
        return f"{self.length}"


def step(maze: np.array, path: Path) -> list[Path]:
    pts = []
    slope_dirs = {
        CELL_DOWN: (1, 0),
        CELL_UP: (-1, 0),
        CELL_LEFT: (0, -1),
        CELL_RIGHT: (0, 1),
    }
    y, x = path.points[-1]
    for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        ny, nx = y + dy, x + dx
        if (ny, nx) in path.points:
            continue
        if maze[ny, nx] == CELL_WALL:
            continue
        if maze[ny, nx] == CELL_EMPTY:
            pts.append((ny, nx))
            continue
        else:
            slope = slope_dirs[maze[ny, nx]]
            # if slope == (dy, dx):
            pts.append((ny, nx))
    ret = []
    for p in pts:
        if p == pts[-1]:
            p2 = path
        else:
            p2 = path.clone()
        p2.points.append(p)
        ret.append(p2)
    return ret


def find_longest(maze: np.array, start: tuple[int, int], stop: tuple[int, int]) -> int:
    p0 = Path()
    p0.points.append(start)
    final = p0
    cur = [p0]
    t0 = time.time()
    while cur:
        now = time.time()
        if now - t0 > 1:
            t0 = now
            print(len(final.points), len(cur), cur[-10:])
        p = cur.pop()
        if p.points[-1] == stop:
            if len(p.points) > len(final.points):
                final = p
            continue
        pp = step(maze, p)
        cur.extend(pp)
    return len(final.points) - 1


class Node:
    def __init__(self, pos: tuple[int, int], final: bool = False):
        self.pos = pos
        self.edges: set[Edge] = set()
        self.final = final

    def __str__(self):
        return f"<{self.pos}: {self.edges}>"


class Edge:
    def __init__(self, n1: Node, n2: Node, weight: int = 1):
        self.n1 = n1
        self.n2 = n2
        self.weight = weight

    def other(self, node):
        return list({self.n1, self.n2} - set([node]))[0]

    def __hash__(self):
        return hash(self.n1.pos) + hash(self.n2.pos)

    def __eq__(self, other):
        return (self.n1 == other.n1 and self.n2 == other.n2) \
            or (self.n1 == other.n2 and self.n2 == other.n1)

    def __repr__(self):
        return f"{self.n1.pos}->{self.n2.pos}:{self.weight}"


def create_graph(maze: np.array, start, stop):
    nodes: dict[tuple[int, int], Node] = {start: Node(start, True), stop: Node(stop, True)}
    for y, line in enumerate(maze):
        if y == 0 or y == maze.shape[0] - 1:
            continue
        for x, val in enumerate(line):
            if val == CELL_WALL:
                continue
            if (y, x) not in nodes:
                nodes[y, x] = Node((y, x))
            n1 = nodes[y, x]
            for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                p = y + dy, x + dx
                if maze[p] == CELL_WALL:
                    continue
                if p not in nodes:
                    nodes[p] = Node(p)
                n2 = nodes[p]
                e = Edge(n1, n2, 1)
                n1.edges.add(e)
                n2.edges.add(e)
    return nodes


def optimize(nodes: dict[tuple[int, int]: Node]):
    while True:
        exit = True
        node = None
        for node in nodes.values():
            if len(node.edges) == 2 and not node.final:
                exit = False
                break
        if exit:
            break
        if len(node.edges) == 2:
            ee = list(node.edges)
            n0 = ee[0].other(node)
            n1 = ee[1].other(node)
            e0 = ee[0]
            e1 = ee[1]
            n0.edges.remove(e0)
            n1.edges.remove(e1)
            e = Edge(n0, n1, e0.weight + e1.weight)
            n0.edges.add(e)
            n1.edges.add(e)
            del nodes[node.pos]


def print_gv(nodes):
    print("digraph {")
    for node in nodes.values():
        for e in node.edges:
            if e.n1 != node:
                continue
            print(f'"{e.n1.pos}" -> "{e.n2.pos}"')
    print("}")


def longest_path(nodes: dict[tuple[int, int], Node], start: tuple[int, int], stop: tuple[int, int]):
    p0 = Path()
    p0.points.append(start)
    paths = [p0]
    longest = p0
    prev_t = time.time()
    while paths:
        now = time.time()
        if now - prev_t > 1:
            prev_t = now
            print(f"{longest.length=} {len(paths)=}")
        path = paths.pop()
        # print(path.points)
        head = path.points[-1]
        if head == stop:
            if path.length > longest.length:
                longest = path
                continue
        node = nodes[head]
        for edge in node.edges:
            n2 = edge.other(node)
            if n2.pos in path.points:
                continue
            p2 = path.clone()
            p2.points.append(n2.pos)
            p2.length += edge.weight
            paths.append(p2)
    return longest.length


def task1():
    fn = "i23a.txt"
    maze = load(fn)
    # print(maze)
    start = (0, 1)
    stop = (maze.shape[0] - 1, maze.shape[1] - 2)
    # cnt = find_longest(maze, start, stop)
    # print(cnt)
    # print_gv(maze, start, stop)
    nodes = create_graph(maze, start, stop)
    # for n in nodes.values():
    #     print(n)
    optimize(nodes)
    # print_gv(nodes)
    ret = longest_path(nodes, start, stop)
    print(ret)
