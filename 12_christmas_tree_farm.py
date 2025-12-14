from aoc import Input, run, TestCase, extract_ints
from enum import IntEnum

TILE = "#"
SHAPE_WIDTH = 3
SHAPE_HEIGHT = 3


class RegionCheck(IntEnum):
    FITS = 1
    DOESNT_FIT = 0
    NEEDS_SOLVER = -1


def count_tiles(shape):
    _present_num, *grid = shape.as_lines()
    return sum(ch == TILE for row in grid for ch in row)


def fits_by_simple_bounds(width, height, num_presents):
    max_presents_lower_bound = (width // SHAPE_WIDTH) * (height // SHAPE_HEIGHT)
    return num_presents <= max_presents_lower_bound


def exceeds_tile_capacity(width, height, shape_quantities, tiles):
    num_tiles_lower_bound = sum(
        tiles * quantity for tiles, quantity in zip(tiles, shape_quantities)
    )
    return num_tiles_lower_bound > width * height


def check_region(region, tiles):
    width, height, *shape_quantities = extract_ints(region)
    num_presents = sum(shape_quantities)

    if fits_by_simple_bounds(width, height, num_presents):
        return RegionCheck.FITS

    if exceeds_tile_capacity(width, height, shape_quantities, tiles):
        return RegionCheck.DOESNT_FIT

    return RegionCheck.NEEDS_SOLVER  # you've been trolled says reddit


def part1_solution(data_file) -> int:
    *shapes, regions = Input(data_file).as_sections()
    tiles = [count_tiles(shape) for shape in shapes]
    return sum([check_region(region, tiles) for region in regions.as_lines()])


if __name__ == "__main__":
    run(
        part1_solution,
        [
            TestCase("data/12_example_01", -3),
            TestCase("data/12_puzzle_input", 463),
        ],
    )
