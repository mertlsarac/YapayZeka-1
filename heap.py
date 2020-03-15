class Heap:
    def __init__(self):
        self.l = []

    def down_heapify(self, root):
        min = root
        left = 2 * root + 1
        right = 2 * root + 2

        if left < len(self.l):
            if self.l[left].f < self.l[min].f:
                min = left

        if right < len(self.l):
            if self.l[right].f < self.l[min].f:
                min = right

        if min != root:
            self.l[min], self.l[root] = self.l[root], self.l[min]
            self.down_heapify(min)

    def up_heapify(self, leaf):
        parent = (leaf - 1) // 2

        if parent >= 0:
            if self.l[leaf].f < self.l[parent].f:
                self.l[leaf], self.l[parent] = self.l[parent], self.l[leaf]
                self.up_heapify(parent)

    def pop(self):
        self.l[0], self.l[len(self.l) - 1] = self.l[len(self.l) - 1], self.l[0]
        end_node = self.l.pop(len(self.l) - 1)
        self.down_heapify(0)
        #print("pop")
        #print([i.f for i in self.l])
        return end_node

    def add(self, node):
        self.l.append(node)
        self.up_heapify(len(self.l) - 1)