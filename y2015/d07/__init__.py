def task1():
    rules = []
    vals: dict[str, int] = {}
    for v in range(65536):
        vals[str(v)] = v
    fn = "y2015/d07/i.txt"
    for line in open(fn):
        l, name = line.strip().split(" -> ")
        l = l.split(" ")
        rules.append((name, l))
        vals[name] = None
        print(name, l)
    while vals["a"] is None:
        for name, rule in rules:
            if vals[name] is not None:
                continue
            val = None
            if len(rule) == 1:
                val = vals[rule[0]]
            elif len(rule) == 2:
                # NOT
                n = rule[1]
                if vals[n] is None:
                    continue
                val = 0xffff ^ vals[n]
            else:
                n1 = rule[0]
                n2 = rule[2]
                v1 = vals[n1]
                v2 = vals[n2]
                if v1 is None or v2 is None:
                    continue
                op = rule[1]
                if op == "AND":
                    val = v1 & v2
                elif op == "OR":
                    val = v1 | v2
                elif op == "LSHIFT":
                    val = (v1 << v2) & 0xffff
                elif op == "RSHIFT":
                    val = v1 >> v2
            vals[name] = val
    print(vals["a"])


def task2():
    rules = []
    vals: dict[str, int] = {}
    for v in range(65536):
        vals[str(v)] = v
    fn = "y2015/d07/i.txt"
    for line in open(fn):
        l, name = line.strip().split(" -> ")
        l = l.split(" ")
        rules.append((name, l))
        vals[name] = None
        print(name, l)
    vals["b"] = 46065
    while vals["a"] is None:
        for name, rule in rules:
            if vals[name] is not None:
                continue
            val = None
            if len(rule) == 1:
                val = vals[rule[0]]
            elif len(rule) == 2:
                # NOT
                n = rule[1]
                if vals[n] is None:
                    continue
                val = 0xffff ^ vals[n]
            else:
                n1 = rule[0]
                n2 = rule[2]
                v1 = vals[n1]
                v2 = vals[n2]
                if v1 is None or v2 is None:
                    continue
                op = rule[1]
                if op == "AND":
                    val = v1 & v2
                elif op == "OR":
                    val = v1 | v2
                elif op == "LSHIFT":
                    val = (v1 << v2) & 0xffff
                elif op == "RSHIFT":
                    val = v1 >> v2
            vals[name] = val
    print(vals["a"])
