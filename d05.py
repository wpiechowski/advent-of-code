import re


re_new = re.compile(r"(\w+)-to-(\w+) map:")
re_map = re.compile(r"(\d+) (\d+) (\d+)")
re_seeds = re.compile(r"seeds: ([0-9 ]+)")


def translate(vals, to_start, from_start, size):
    ret = []
    to_remove = []
    for v in vals:
        if from_start <= v < from_start + size:
            to_remove.append(v)
            ret.append(v - from_start + to_start)
    for v in to_remove:
        vals.remove(v)
    return ret


def task1():
    cur_vals = []
    next_vals = []
    for line in open("i05a.txt"):
        line = line.strip()
        m = re_seeds.match(line)
        if m:
            cur_vals = list(map(int, m[1].split(" ")))
            continue
        m = re_new.match(line)
        if m:
            next_vals.extend(cur_vals)
            cur_vals = next_vals
            next_vals = []
            continue
        m = re_map.match(line)
        if m:
            to_start, from_start, size = list(map(int, m.group(1, 2, 3)))
            print(to_start, from_start, size)
            next_vals.extend(translate(cur_vals, to_start, from_start, size))
    next_vals.extend(cur_vals)
    print(sorted(next_vals))


"""
seeds [sa.......sa + sc)
"""


def translate2(ranges_in, ranges_out, to_start, from_start, size):
    ret_in = []
    while ranges_in:
        sa, sc = ranges_in.pop(0)
        sb = sa + sc
        ma = from_start
        mb = from_start + size
        if sb <= ma or sa >= mb:
            ret_in.append([sa, sc])
            continue
        if sa < ma:
            ranges_in.append([sa, ma - sa])
            ranges_in.append([ma, (sb - sa) - (ma - sa)])
            continue
        if sb > mb:
            ranges_in.append([sa, mb - sa])
            ranges_in.append([mb, sb - mb])
            continue
        # sa...sb should be completely in ma..mb
        ranges_out.append([to_start + sa - ma, sc])
    return ret_in


def task2():
    ranges_in = []
    ranges_out = []
    for line in open("i05a.txt"):
        line = line.strip()
        m = re_seeds.match(line)
        if m:
            cur_vals = list(map(int, m[1].split(" ")))
            for a, b in zip(cur_vals[::2], cur_vals[1::2]):
                ranges_in.append([a, b])
            continue
        m = re_new.match(line)
        if m:
            ranges_out.extend(ranges_in)
            ranges_in = ranges_out
            ranges_out = []
            continue
        m = re_map.match(line)
        if m:
            to_start, from_start, size = list(map(int, m.group(1, 2, 3)))
            ranges_in = translate2(ranges_in, ranges_out, to_start, from_start, size)
    ranges_out.extend(ranges_in)
    ranges_out.sort(key=lambda x:x[0])
    print(ranges_out)
