from aoc import read_data, run, TestCase


def parse(data_file):
    """Parse comma-separated ranges like '1-100, 200-300' into list of tuples."""
    data = read_data(data_file)
    ranges = []
    for range_str in data.split(","):
        start, end = map(int, range_str.strip().split("-"))
        ranges.append((start, end))
    return ranges


def has_pattern_repeated_exactly_twice(number):
    """
    Check if pattern is repeated EXACTLY twice.

    Examples:
        55 (5 twice) -> True
        6464 (64 twice) -> True
        111 (1 three times) -> False
    """
    digits = str(number)

    if len(digits) % 2 != 0:
        return False

    mid = len(digits) // 2
    first_half = digits[:mid]
    second_half = digits[mid:]
    return first_half == second_half


def has_repeating_pattern(number):
    """
    Check if pattern is repeated AT LEAST twice.

    Examples:
        55 (5 twice) -> True
        111 (1 three times) -> True
        12341234 (1234 twice) -> True
    """
    digits = str(number)
    length = len(digits)

    for pattern_length in range(1, length // 2 + 1):
        if length % pattern_length == 0:
            pattern = digits[:pattern_length]
            repetitions = length // pattern_length
            if pattern * repetitions == digits:
                return True

    return False


def sum_of_invalid_ids_part1(data_file):
    """Sum all IDs with patterns repeated exactly twice."""
    ranges = parse(data_file)
    total = 0

    for start, end in ranges:
        for number in range(start, end + 1):
            if has_pattern_repeated_exactly_twice(number):
                total += number

    return total


def sum_of_invalid_ids_part2(data_file):
    """Sum all IDs with any repeating pattern."""
    ranges = parse(data_file)
    total = 0

    for start, end in ranges:
        for number in range(start, end + 1):
            if has_repeating_pattern(number):
                total += number

    return total


if __name__ == "__main__":
    TESTS = [
        TestCase("02_example_01"),
        TestCase("02_puzzle_input"),
    ]

    run(sum_of_invalid_ids_part1, TESTS, part="part1")
    run(sum_of_invalid_ids_part2, TESTS, part="part2")
