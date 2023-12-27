import numpy as np
import heapq
import copy


def load_maze(f):
    ret = []
    for line in f:
        ret.append([])
        for ch in line.strip():
            ret[-1].append(int(ch))
    return np.array(ret, dtype=int)


class PathPoint:
    def __init__(self, x: int, y: int, dx: int, dy: int, cont: int):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.cont = cont

    def __repr__(self):
        return f"({self.x},{self.y}/{self.cont})"

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def tuplize(self):
        return self.x, self.y, self.dx, self.dy, self.cont


class Path:
    def __init__(self):
        self.path: list[PathPoint] = []
        self.heat_sum = 0

    def __eq__(self, other):
        return self.heat_sum == other.heat_sum

    def __lt__(self, other):
        return self.heat_sum < other.heat_sum

    def __deepcopy__(self, memodict={}):
        p = Path()
        p.path = copy.copy(self.path)
        p.heat_sum = self.heat_sum
        return p

    def __repr__(self):
        return f"[{self.heat_sum} {len(self.path)}: {self.path}]"


def new_paths(path: Path, maze: np.array) -> list[Path]:
    lp = path.path[-1]
    ret = []
    for d in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        if (-lp.dx, -lp.dy) == d:
            continue
        x, y = lp.x + d[0], lp.y + d[1]
        if x < 0 or x >= maze.shape[1]:
            continue
        if y < 0 or y >= maze.shape[0]:
            continue
        same_dir = (lp.dx, lp.dy) in (d, (0, 0))
        c = lp.cont + 1 if same_dir else 2
        if 0:
            if c > 4:
                continue
        else:
            if lp.cont <= 4 and not same_dir:
                continue
            if lp.cont > 10 and same_dir:
                continue

        pp = PathPoint(x, y, d[0], d[1], c)
        if pp in path.path:
            continue
        p = copy.deepcopy(path)
        p.heat_sum += maze[y, x]
        p.path.append(pp)
        ret.append(p)
    return ret


def print_path(p: Path, m: np.array):
    fp = PathPoint(0, 0, 0, 0, 0)
    heat = 0
    for y, line in enumerate(m):
        text = ""
        fp.y = y
        for x, val in enumerate(line):
            fp.x = x
            text += str(val)
            text += "*" if fp in p.path else " "
            if fp in p.path and (fp.x, fp.y) != (0, 0):
                heat += m[y, x]
        print(text)
    print(heat)


def task1():
    fn = "i17a.txt"
    m = load_maze(open(fn))
    print(m)
    paths = [Path()]
    paths[-1].path.append(PathPoint(m.shape[1] - 1, m.shape[0] - 1, 0, 0, 1))
    been = set()
    heapq.heapify(paths)
    while paths:
        p = heapq.heappop(paths)
        print(p.heat_sum, len(paths))
        # print(p)
        pp = p.path[-1]
        if (pp.x, pp.y) == (0, 0):
            print(p.heat_sum)
            break
        pt = pp.tuplize()
        if pt in been:
            continue
        been.add(pt)
        p2 = new_paths(p, m)
        for p in p2:
            heapq.heappush(paths, p)
    print_path(p, m)
