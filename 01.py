from aoc import read_data_as_lines, run

WHEEL_SIZE = 100
START_POSITION = 50


def parse(data):
    lines = read_data_as_lines("01", data)
    return [(line[0], int(line[1:])) for line in lines]


def count_zero_crossings(position, distance):
    if position == 0:
        return distance // WHEEL_SIZE
    elif distance >= position:
        return (distance - position) // WHEEL_SIZE + 1
    else:
        return 0


def rotate_left(position, distance):
    return (position - distance) % WHEEL_SIZE


def rotate_right(position, distance):
    return (position + distance) % WHEEL_SIZE


def rotations_ending_on_zero(data):
    rotations = parse(data)
    position = START_POSITION
    count = 0

    for direction, distance in rotations:
        position = (
            rotate_left(position, distance)
            if direction == "L"
            else rotate_right(position, distance)
        )
        if position == 0:
            count += 1

    return count


def number_of_clicks_on_zero(data):
    rotations = parse(data)
    position = START_POSITION
    count = 0

    for direction, distance in rotations:
        if direction == "L":
            count += count_zero_crossings(position, distance)
            position = rotate_left(position, distance)
        else:  # "R"
            count += (position + distance) // WHEEL_SIZE
            position = rotate_right(position, distance)

    return count


if __name__ == "__main__":
    # Part 1
    run(rotations_ending_on_zero, [("example_01", 3), ("puzzle_input", 1007)])

    # Part 2
    run(number_of_clicks_on_zero, [("example_01", 6), ("puzzle_input", 5820)])
