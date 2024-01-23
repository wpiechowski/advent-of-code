import heapq


def print_gv(fn: str):
    print("digraph {")
    for line in open(fn):
        n1, nn = line.strip().split(": ")
        for n2 in nn.split(" "):
            print(f"{n1} -> {n2}")
    print("}")


class Edge:
    def __init__(self, n1, n2):
        self.n1 = n1
        self.n2 = n2

    def __eq__(self, other):
        return (self.n1 == other.n1 and self.n2 == other.n2) or (self.n1 == other.n2 and self.n2 == other.n1)

    def __hash__(self):
        return hash(self.n1) + hash(self.n2)

    def other(self, node):
        return list({self.n1, self.n2} - set([node]))[0]


class Node:
    def __init__(self, name: str):
        self.name = name
        self.edges = set()

    def add_edge(self, e: Edge):
        self.edges.add(e)

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return f"Node({self.name})"

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.name < other.name


def load(fn: str) -> dict[str, Node]:
    nodes: dict[str, Node] = {}
    for line in open(fn):
        n1, nn = line.strip().split(": ")
        if n1 not in nodes:
            nodes[n1] = Node(n1)
        for n2 in nn.split(" "):
            if n2 not in nodes:
                nodes[n2] = Node(n2)
            e = Edge(nodes[n1], nodes[n2])
            nodes[n1].add_edge(e)
            nodes[n2].add_edge(e)
    return nodes


def find_shortest_paths(start: Node):
    visit = {start}
    q = [(0, start, [])]
    while q:
        cnt, here, path = heapq.heappop(q)
        for e in here.edges:
            n2 = e.other(here)
            if n2 in visit:
                continue
            p2 = path.copy()
            p2.append(e)
            item = cnt + 1, n2, p2
            visit.add(n2)
            yield p2
            heapq.heappush(q, item)


def find_paths(nodes: dict[str, Node]):
    edge_counts: dict[Edge, int] = {}
    for n1 in sorted(nodes.values()):
        print("find for", n1)
        for path in find_shortest_paths(n1):
            # print(path)
            for e in path:
                if e not in edge_counts:
                    edge_counts[e] = 0
                edge_counts[e] += 1
    elist = [(v, e.n1.name, e.n2.name) for e, v in edge_counts.items()]
    elist.sort(reverse=True)
    print(elist)
    return elist[:3]


def count_groups(nodes: dict[str, Node]):
    groups: list[set[Node]] = []
    taken: set[Node] = set()
    while True:
        for node in nodes.values():
            if node not in taken:
                g = set()
                q = [node]
                while q:
                    n = q.pop()
                    if n in g:
                        continue
                    g.add(n)
                    for e in n.edges:
                        n2 = e.other(n)
                        if n2 not in g:
                            q.append(n2)
                groups.append(g)
                taken |= g
                break
        else:
            break
    for g in groups:
        print(len(g))


def task1():
    fn = "i25a.txt"
    nodes = load(fn)
    # print_gv(nodes)
    # print_gv(fn)
    # print(nodes)
    # e3 = find_paths(nodes)
    e3 = [
        (1, "xhl", "shj"),
        (2, "fxk", "bcf"),
        (3, "zgp", "cgt"),
    ]
    for _, n1, n2 in e3:
        e = Edge(nodes[n1], nodes[n2])
        e.n1.edges.remove(e)
        e.n2.edges.remove(e)
    count_groups(nodes)


"""
xhl-shj
fxk-bcf
zgp-cgt
"""
