from aoc import Coord, Grid, Input, run, TestCase


def parse(args):
    return Input(args).as_grid()


def count_adjacent_rolls(grid, position):
    neighbors = position.neighbors(grid.max_bounds, directions=Coord.DIRECTIONS_ALL)
    return sum(1 for neighbor in neighbors if grid[neighbor] == "@")


def is_removable(grid, position):
    return grid[position] == "@" and count_adjacent_rolls(grid, position) < 4


def find_removable_rolls(grid):
    return {pos for pos, _ in grid.coords() if is_removable(grid, pos)}


def count_accessible_rolls(args):
    grid = parse(args)
    return len(find_removable_rolls(grid))


def count_total_removable_rolls(args):
    grid = parse(args)
    total_removed = 0

    while removable := find_removable_rolls(grid):
        for pos in removable:
            grid[pos] = "."
        total_removed += len(removable)

    return total_removed


if __name__ == "__main__":
    run(
        count_accessible_rolls,
        [
            TestCase("data/04_example_01", 13),
            TestCase("data/04_puzzle_input", 1395),
        ],
    )
    run(
        count_total_removable_rolls,
        [
            TestCase("data/04_example_01", 43),
            TestCase("data/04_puzzle_input", 8451),
        ],
    )
