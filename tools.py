import inspect
import re


def get_path():
    re_path = re.compile(r"y(\d{4})\\d(\d{2})\\")
    stack = inspect.stack()
    for entry in stack:
        f = entry.filename
        for m in re_path.finditer(f):
            return m[0]
    return ""


def get_lines(fn: str):
    for line in open(get_path() + fn):
        yield line.strip()


def get_re_lines(fn: str, rx: str):
    re_line = re.compile(rx)
    for line in get_lines(fn):
        m = re_line.match(line)
        if m:
            yield m.groups()


def test():
    get_path()


if __name__ == "__main__":
    test()
