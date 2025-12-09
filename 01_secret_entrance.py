from aoc import Input, run, TestCase

WHEEL_SIZE = 100
START_POSITION = 50


def parse(data_file):
    lines = Input(data_file).as_lines()
    return [(line[0], int(line[1:])) for line in lines]


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


def rotations_ending_on_zero(data_file):
    rotations = parse(data_file)
    position = START_POSITION
    count = 0

    for direction, distance in rotations:
        if direction == "L":
            position = rotate_left(position, distance)
        else:
            position = rotate_right(position, distance)

        if position == 0:
            count += 1

    return count


def number_of_clicks_on_zero(data_file):
    rotations = parse(data_file)
    position = START_POSITION
    total_clicks = 0

    for direction, distance in rotations:
        if direction == "L":
            total_clicks += count_zero_crossings_left(position, distance)
            position = rotate_left(position, distance)
        else:  # "R"
            total_clicks += count_zero_crossings_right(position, distance)
            position = rotate_right(position, distance)

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
