from itertools import combinations

from aoc import Input, run, TestCase
from aoc.d2 import Coord, Dimension, Grid
from aoc.graph import flood_fill_mark


def parse(data_file: str) -> list[Coord]:
    lines = Input(data_file).as_lines()
    return [Coord(*map(int, line.split(","))) for line in lines]


def area(a: Coord, b: Coord):
    width = abs(a.col - b.col) + 1
    height = abs(a.row - b.row) + 1
    return width * height


"""
 Imagine you have these red points:
    (7, 1), (11, 1), (11, 7), (9, 7), (9, 5), (2, 5), (2, 3), (7, 3)

 Original coordinate space (12 × 8):
        0  1  2  3  4  5  6  7  8  9 10 11
     ┌─────────────────────────────────────┐
   0 │  .  .  .  .  .  .  .  .  .  .  .  . │
   1 │  .  .  .  .  .  .  .  #  .  .  #  . │
   2 │  .  .  .  .  .  .  .  .  .  .  .  . │
   3 │  .  .  #  .  .  .  .  #  .  .  .  . │
   4 │  .  .  .  .  .  .  .  .  .  .  .  . │
   5 │  .  .  #  .  .  .  .  .  .  #  .  . │
   6 │  .  .  .  .  .  .  .  .  .  .  .  . │
   7 │  .  .  .  .  .  .  .  .  .  #  .  # │
     └─────────────────────────────────────┘
      Points at x = { 2, 7, 9, 11 } for total of 4 required x "cols"
      Points at y = { 1, 3, 5, 7 } for total of 4 required y "rows"

  Compressed coordinate space (4 × 4):
        0  1  2  3
     ┌─────────────┐
   0 │  .  #  .  # │
   1 │  #  #  .  . │
   2 │  #  .  #  . │
   3 │  .  .  #  # │
     └─────────────┘
 
 ReIndex Original → Compressed
 -----------------------------
  X: 2  → 0  |  Y: 1  →  0
  X: 7  → 1  |  Y: 3  →  1
  X: 9  → 2  |  Y: 5  →  2
  X: 11 → 3  |  Y: 7  →  3
"""


def compress_coordinates(
    coords: list[Coord],
) -> tuple[dict[int, int], dict[int, int], list[int], list[int]]:
    unique_x = sorted(set(c.x for c in coords))
    unique_y = sorted(set(c.y for c in coords))

    x_to_compressed = {x: i for i, x in enumerate(unique_x)}
    y_to_compressed = {y: i for i, y in enumerate(unique_y)}

    return x_to_compressed, y_to_compressed, unique_x, unique_y


def create_boundary_grid(
    coords: list[Coord], x_map: dict[int, int], y_map: dict[int, int]
) -> Grid:
    max_cx = max(x_map.values())
    max_cy = max(y_map.values())
    grid = Grid.create(Dimension(max_cx + 1, max_cy + 1), ".")

    closed_path = [*coords, coords[0]]
    for p1, p2 in zip(closed_path, closed_path[1:]):
        c1 = (x_map[p1.x], y_map[p1.y])
        c2 = (x_map[p2.x], y_map[p2.y])

        if c1[0] == c2[0]:
            for y in range(min(c1[1], c2[1]), max(c1[1], c2[1]) + 1):
                grid[Coord(c1[0], y)] = "#"
        else:
            for x in range(min(c1[0], c2[0]), max(c1[0], c2[0]) + 1):
                grid[Coord(x, c1[1])] = "#"

    return grid


def flood_fill_interior(
    grid: Grid, x_map: dict[int, int], y_map: dict[int, int], coords: list[Coord]
) -> None:
    seed_cx = (x_map[coords[0].x] + x_map[coords[2].x]) // 2
    seed_cy = (y_map[coords[0].y] + y_map[coords[2].y]) // 2
    seed = Coord(seed_cx, seed_cy)

    if grid[seed] != ".":
        seed = grid.find_first(".")
        if seed is None:
            return

    flood_fill_mark(grid, seed, {"."}, "I")


def is_rectangle_valid(
    grid: Grid,
    x_map: dict[int, int],
    y_map: dict[int, int],
    c1: Coord,
    c2: Coord,
    unique_x: list[int],
    unique_y: list[int],
) -> bool:
    min_x, max_x = min(c1.x, c2.x), max(c1.x, c2.x)
    min_y, max_y = min(c1.y, c2.y), max(c1.y, c2.y)

    rect_x = [x for x in unique_x if min_x <= x <= max_x]
    rect_y = [y for y in unique_y if min_y <= y <= max_y]

    for x in rect_x:
        for y in rect_y:
            if grid[Coord(x_map[x], y_map[y])] == ".":
                return False

    return True


def largest_rectangle_area(data_file: str) -> int:
    coords = parse(data_file)
    return max(area(a, b) for a, b in combinations(coords, 2))


def largest_rectangle_area_constrained(data_file: str) -> int:
    coords = parse(data_file)

    x_map, y_map, unique_x, unique_y = compress_coordinates(coords)

    grid = create_boundary_grid(coords, x_map, y_map)

    flood_fill_interior(grid, x_map, y_map, coords)

    max_area = 0
    for i in range(len(coords)):
        for j in range(i + 1, len(coords)):
            if is_rectangle_valid(
                grid, x_map, y_map, coords[i], coords[j], unique_x, unique_y
            ):
                max_area = max(max_area, area(coords[i], coords[j]))

    return max_area


if __name__ == "__main__":
    run(
        largest_rectangle_area,
        [
            TestCase("data/09_example_01", 50),
            TestCase("data/09_puzzle_input", 4729332959),
        ],
    )

    run(
        largest_rectangle_area_constrained,
        [
            TestCase("data/09_example_01", 24),
            TestCase("data/09_puzzle_input", 1474477524),
        ],
    )
