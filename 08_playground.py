import heapq
import math
from typing import NamedTuple

from aoc import Input, run, TestCase, UnionFind
from aoc.d3 import Coord


class Edge(NamedTuple):
    distance: int
    i: int
    j: int


class CoordPair(NamedTuple):
    a: Coord
    b: Coord


def parse(data_file: str) -> list[Coord]:
    lines = Input(data_file).as_delimited_lines(separator=",", converter=int)
    return [Coord(*line) for line in lines]


def compute_distances(coords: list[Coord]) -> list[Edge]:
    n = len(coords)

    return sorted(
        Edge(coords[i].squared_distance(coords[j]), i, j)
        for i in range(n)
        for j in range(i + 1, n)
    )


def product_of_three_largest(sizes: list[int]) -> int:
    return math.prod(heapq.nlargest(3, sizes))


def build_connected_components(
    num_coords: int, distances: list[Edge], num_connections: int
) -> UnionFind:
    uf = UnionFind(num_coords)
    for _, i, j in distances[:num_connections]:
        uf.union(i, j)
    return uf


def find_final_connecting_edge(coords: list[Coord], distances: list[Edge]) -> CoordPair:
    uf = UnionFind(len(coords))
    return next(
        CoordPair(coords[i], coords[j])
        for _, i, j in distances
        if uf.union(i, j) and uf.count_components() == 1
    )


def three_largest_circuits(data_file: str, num_connections: int) -> int:
    coords = parse(data_file)
    distances = compute_distances(coords)
    uf = build_connected_components(len(coords), distances, num_connections)
    return product_of_three_largest(uf.get_component_sizes())


def last_connection_product(data_file: str) -> int:
    coords = parse(data_file)
    distances = compute_distances(coords)
    pair = find_final_connecting_edge(coords, distances)
    return pair.a.x * pair.b.x


if __name__ == "__main__":
    run(
        three_largest_circuits,
        [
            TestCase(["data/08_example_01", 10], 40),
            TestCase(["data/08_puzzle_input", 1000], 131150),
        ],
    )

    run(
        last_connection_product,
        [
            TestCase("data/08_example_01", 25272),
            TestCase("data/08_puzzle_input", 2497445),
        ],
    )
