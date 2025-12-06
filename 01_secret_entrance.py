from aoc import read_data_as_lines, run, TestCase

WHEEL_SIZE = 100
START_POSITION = 50


def parse(data_file):
    lines = read_data_as_lines(data_file)
    rotations = []
    for line in lines:
        direction = line[0]
        distance = int(line[1:])
        rotations.append((direction, distance))
    return rotations


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
    TESTS = [
        TestCase("01_example_01"),
        TestCase("01_puzzle_input"),
    ]

    run(rotations_ending_on_zero, TESTS, part="part1")
    run(number_of_clicks_on_zero, TESTS, part="part2")
