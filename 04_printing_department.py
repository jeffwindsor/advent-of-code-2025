from aoc import (
    Coord,
    grid_coords,
    grid_get,
    grid_max_bounds,
    grid_set,
    read_data_as_char_grid,
    run,
    TestCase,
)


def parse(data_file):
    return read_data_as_char_grid(data_file)


def count_adjacent_rolls(grid, position):
    max_bounds = grid_max_bounds(grid)
    neighbors = position.neighbors(max_bounds, directions=Coord.DIRECTIONS_ALL)
    return sum(1 for neighbor in neighbors if grid_get(grid, neighbor) == "@")


def is_removable(grid, position):
    return grid_get(grid, position) == "@" and count_adjacent_rolls(grid, position) < 4


def find_removable_rolls(grid):
    return {pos for pos, _ in grid_coords(grid) if is_removable(grid, pos)}


def count_accessible_rolls(data_file):
    grid = parse(data_file)
    return len(find_removable_rolls(grid))


def count_total_removable_rolls(data_file):
    grid = parse(data_file)
    total_removed = 0

    while removable := find_removable_rolls(grid):
        for pos in removable:
            grid_set(grid, pos, ".")
        total_removed += len(removable)

    return total_removed


if __name__ == "__main__":
    TESTS = [
        TestCase("04_example_01"),
        TestCase("04_puzzle_input"),
    ]

    run(count_accessible_rolls, TESTS, part="part1")
    run(count_total_removable_rolls, TESTS, part="part2")
