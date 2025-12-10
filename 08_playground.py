# classic graph connectivity challenge with some interesting twists
# Part 1 - Propsed Steps:
#  1. Parse coordinates into list of tuples
#  2. Calculate all N×(N-1)/2 pairwise squared distances
#  3. Sort pairs by distance
#  4. Process first 1000 pairs with Union-Find
#  5. Extract all component sizes
#  6. Return product of 3 largest

from aoc import Input, run, TestCase
import heapq
import math


class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.size = [1] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return

        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
            self.size[root_y] += self.size[root_x]
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
            self.size[root_x] += self.size[root_y]
        else:
            self.parent[root_y] = root_x
            self.size[root_x] += self.size[root_y]
            self.rank[root_x] += 1

    def get_component_sizes(self):
        sizes = {}
        for i in range(len(self.parent)):
            root = self.find(i)
            if root not in sizes:
                sizes[root] = self.size[root]
        return list(sizes.values())


def parse(args):
    return Input(args).as_delimited_lines(separator=",", converter=int)


def squared_distance(p1, p2):
    return sum((a - b) ** 2 for a, b in zip(p1, p2))


def three_largest_circuits(args, num_connections):
    coords = parse(args)
    n = len(coords)

    distances = []
    for i in range(n):
        for j in range(i + 1, n):
            dist = squared_distance(coords[i], coords[j])
            distances.append((dist, i, j))

    distances.sort()

    uf = UnionFind(n)
    for k in range(min(num_connections, len(distances))):
        _, i, j = distances[k]
        uf.union(i, j)

    sizes = uf.get_component_sizes()
    return math.prod(heapq.nlargest(3, sizes))


if __name__ == "__main__":
    run(
        three_largest_circuits,
        [
            TestCase(["data/08_example_01", 10], 40),
        ],
    )

    run(
        three_largest_circuits,
        [
            TestCase(["data/08_puzzle_input", 1000], 131150),
        ],
    )
