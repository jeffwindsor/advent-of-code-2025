from collections import defaultdict
from typing import NamedTuple
from aoc import Input, run, TestCase, Grid, Coord

START = "S"
SPLITTER = "^"


class BeamData(NamedTuple):
    grid: Grid
    start: Coord
    splitters_by_row: dict[int, set[int]]


def parse(args: str) -> BeamData:
    grid = Input(args).as_grid()
    start = grid.find_first(START)
    if start is None:
        raise ValueError(f"No start position '{START}' found in grid")

    splitters_by_row = defaultdict(set)
    for coord, value in grid.coords():
        if value == SPLITTER:
            splitters_by_row[coord.row].add(coord.col)

    return BeamData(grid, start, splitters_by_row)


def unique_splitters_visited(args: str) -> int:
    data = parse(args)

    beam_columns = {data.start.col}
    splitters_hit = set()

    for row in range(data.start.row + 1, data.grid.max_bounds.row + 1):
        hits = beam_columns & data.splitters_by_row.get(row, set())
        splitters_hit.update(Coord(row, col) for col in hits)

        beam_columns = (beam_columns - hits) | {
            neighbor
            for col in hits
            for neighbor in (col - 1, col + 1)
            if 0 <= neighbor <= data.grid.max_bounds.col
        }
        if not beam_columns:
            break

    return len(splitters_hit)


def quantum_beams(args: str) -> int:
    data = parse(args)

    beams = {data.start.col: 1}

    for row in range(data.start.row + 1, data.grid.max_bounds.row + 1):
        next_beams = defaultdict(int)

        for col, count in beams.items():
            if col in data.splitters_by_row.get(row, set()):
                for neighbor in (col - 1, col + 1):
                    if 0 <= neighbor <= data.grid.max_bounds.col:
                        next_beams[neighbor] += count
            else:
                next_beams[col] += count

        beams = dict(next_beams)
        if not beams:
            break

    return sum(beams.values())


if __name__ == "__main__":
    run(
        unique_splitters_visited,
        [
            TestCase("data/07_example_01", 21),
            TestCase("data/07_puzzle_input", 1573),
        ],
    )

    run(
        quantum_beams,
        [
            TestCase("data/07_example_01", 40),
            TestCase("data/07_puzzle_input", 15093663987272),
        ],
    )
