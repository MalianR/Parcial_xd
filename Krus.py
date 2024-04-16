class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x != root_y:
            if self.rank[root_x] < self.rank[root_y]:
                root_x, root_y = root_y, root_x
            self.parent[root_y] = root_x
            if self.rank[root_x] == self.rank[root_y]:
                self.rank[root_x] += 1

def kruskal(edges, n):
    edges.sort(key=lambda x: x[2])
    mst = []
    uf = UnionFind(n)
    for edge in edges:
        u, v, weight = edge
        if uf.find(u) != uf.find(v):
            mst.append(edge)
            uf.union(u, v)
    return mst

# Ejemplo de uso
edges = [(0, 1, 4), (0, 7, 8), (1, 2, 8), (1, 7, 11), (2, 3, 7),
         (2, 8, 2), (2, 5, 4), (3, 4, 9), (3, 5, 14), (4, 5, 10),
         (5, 6, 2), (6, 7, 1), (6, 8, 6), (7, 8, 7)]
mst = kruskal(edges, 9)
print("Árbol de Expansión Mínima (Kruskal):", mst)
