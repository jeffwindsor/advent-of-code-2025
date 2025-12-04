from aoc import (
    Coord,
    grid_coords,
    grid_get,
    grid_max_bounds,
    read_data_as_char_grid,
    run,
    TestCase,
)


def parse(data_file):
    return read_data_as_char_grid(data_file)


def count_adjacent_rolls(grid, position):
    max_bounds = grid_max_bounds(grid)
    neighbors = position.neighbors(max_bounds, directions=Coord.DIRECTIONS_ALL)
    return sum(1 for neighbor in neighbors if grid_get(grid, neighbor) == '@')


def count_accessible_rolls(data_file):
    grid = parse(data_file)
    accessible = 0

    for position, value in grid_coords(grid):
        if value == '@':
            adjacent_rolls = count_adjacent_rolls(grid, position)
            if adjacent_rolls < 4:
                accessible += 1

    return accessible


if __name__ == "__main__":
    run(count_accessible_rolls, [
        TestCase("04_example_01", 13),
        TestCase("04_puzzle_input", 1395),
    ])
