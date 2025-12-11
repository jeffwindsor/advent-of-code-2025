from itertools import combinations

from aoc import Input, run, TestCase
from aoc.d2 import Coord


def parse(data_file: str) -> list[Coord]:
    lines = Input(data_file).as_lines()
    return [Coord(*map(int, line.split(","))) for line in lines]


def area(a: Coord, b: Coord):
    width = abs(a.col - b.col) + 1
    height = abs(a.row - b.row) + 1
    return width * height


def largest_rectangle_area(data_file: str) -> int:
    coords = parse(data_file)
    return max(area(a, b) for a, b in combinations(coords, 2))


if __name__ == "__main__":
    run(
        largest_rectangle_area,
        [
            TestCase("data/09_example_01", 50),
            TestCase("data/09_puzzle_input", 4729332959),
        ],
    )
