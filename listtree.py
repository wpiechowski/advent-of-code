class ListTree:
    def __init__(self, width: int = 16, up = None):
        self.width = width
        self.up = up
        self.count = 0
        self.is_leaf = True
        self.subs = []
        self.vals = []

    def get(self, index: int):
        if self.is_leaf:
            return self.vals[index]
        for sub in self.subs:
            if sub.count <= index:
                index -= sub.count
                continue
            return sub.get(index)

    def insert(self, pos: int, val):
        if self.is_leaf:
            self.vals.insert(pos, val)
            if len(self.vals) > self.width:
                # need to spill
    def append(self, val):
        if self.is_leaf:
            self.vals.append(val)
        else:
            pass
            # TODO
        n = self
        while n:
            n.count += 1
            n = n.up
