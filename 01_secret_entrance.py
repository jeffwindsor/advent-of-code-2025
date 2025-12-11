from aoc import Input, run, TestCase
from typing import NamedTuple

WHEEL_SIZE = 100
START_POSITION = 50


class Rotation(NamedTuple):
    direction: str
    distance: int


def parse(args):
    lines = Input(args).as_lines()
    return [Rotation(line[0], int(line[1:])) for line in lines]


def count_zero_crossings_left(position, distance):
    if position == 0:
        return distance // WHEEL_SIZE
    elif distance >= position:
        return (distance - position) // WHEEL_SIZE + 1
    else:
        return 0


def count_zero_crossings_right(position, distance):
    return (position + distance) // WHEEL_SIZE


def rotate_left(position, distance):
    return (position - distance) % WHEEL_SIZE


def rotate_right(position, distance):
    return (position + distance) % WHEEL_SIZE


def rotations_ending_on_zero(args):
    rotations = parse(args)
    position = START_POSITION
    count = 0

    for rotation in rotations:
        if rotation.direction == "L":
            position = rotate_left(position, rotation.distance)
        else:
            position = rotate_right(position, rotation.distance)

        if position == 0:
            count += 1

    return count


def number_of_clicks_on_zero(args):
    rotations = parse(args)
    position = START_POSITION
    total_clicks = 0

    for rotation in rotations:
        if rotation.direction == "L":
            total_clicks += count_zero_crossings_left(position, rotation.distance)
            position = rotate_left(position, rotation.distance)
        else:  # "R"
            total_clicks += count_zero_crossings_right(position, rotation.distance)
            position = rotate_right(position, rotation.distance)

    return total_clicks


if __name__ == "__main__":
    run(
        rotations_ending_on_zero,
        [
            TestCase("data/01_example_01", 3),
            TestCase("data/01_puzzle_input", 1007),
        ],
    )
    run(
        number_of_clicks_on_zero,
        [
            TestCase("data/01_example_01", 6),
            TestCase("data/01_puzzle_input", 5820),
        ],
    )
