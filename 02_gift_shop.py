from aoc import read_data, extract_ints, run, TestCase


def parse(data_file):
    ranges = read_data(data_file).split(",")
    return [tuple(extract_ints(r)) for r in ranges]


def has_pattern_repeated_exactly_twice(number):
    digits = str(number)

    if len(digits) % 2 != 0:
        return False

    mid = len(digits) // 2
    left = digits[:mid]
    right = digits[mid:]
    return left == right


def has_repeating_pattern(number):
    digits = str(number)
    length = len(digits)

    for pattern_length in range(1, length // 2 + 1):
        if length % pattern_length == 0:
            pattern = digits[:pattern_length]
            repetitions = length // pattern_length
            if pattern * repetitions == digits:
                return True

    return False


def sum_matching_numbers(data_file, predicate):
    ranges = parse(data_file)
    return sum(
        number
        for start, end in ranges
        for number in range(start, end + 1)
        if predicate(number)
    )


def sum_of_invalid_ids1(data_file):
    return sum_matching_numbers(data_file, has_pattern_repeated_exactly_twice)


def sum_of_invalid_ids2(data_file):
    return sum_matching_numbers(data_file, has_repeating_pattern)


if __name__ == "__main__":
    TESTS = [
        TestCase("02_example_01"),
        TestCase("02_puzzle_input"),
    ]

    run(sum_of_invalid_ids1, TESTS, part="part1")
    run(sum_of_invalid_ids2, TESTS, part="part2")
