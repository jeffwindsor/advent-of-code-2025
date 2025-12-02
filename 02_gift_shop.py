from aoc import read_data, run, TestCase


def parse(data_file):
    data = read_data(data_file)
    ranges = []
    for range_str in data.split(","):
        start, end = map(int, range_str.strip().split("-"))
        ranges.append((start, end))
    return ranges


def is_invalid_id1(n):
    """
    Part 1: Check if pattern is repeated EXACTLY twice.

    Examples:
        55 (5 twice) -> True
        6464 (64 twice) -> True
        111 (1 three times) -> False
    """
    s = str(n)

    # Must have even length to split in half
    if len(s) % 2 != 0:
        return False

    # Split in half and compare
    mid = len(s) // 2
    return s[:mid] == s[mid:]


def is_invalid_id2(n):
    """
    Part 2: Check if pattern is repeated AT LEAST twice.

    Examples:
        55 (5 twice) -> True
        111 (1 three times) -> True
        12341234 (1234 twice) -> True
    """
    value = str(n)
    length = len(value)

    # Try all pattern lengths that allow at least 2 repetitions
    for pattern_len in range(1, length // 2 + 1):
        if length % pattern_len == 0:  # Pattern length must divide evenly
            pattern = value[:pattern_len]
            if pattern * (length // pattern_len) == value:
                return True

    return False


def sum_of_invalid_ids1(data_file):
    ranges = parse(data_file)
    total = 0

    for start, end in ranges:
        for num in range(start, end + 1):
            if is_invalid_id1(num):
                total += num

    return total


def sum_of_invalid_ids2(data_file):
    ranges = parse(data_file)
    total = 0

    for start, end in ranges:
        for num in range(start, end + 1):
            if is_invalid_id2(num):
                total += num

    return total


if __name__ == "__main__":
    # Part 1
    run(
        sum_of_invalid_ids1,
        [
            TestCase("02_example_01", 1227775554),
            TestCase("02_puzzle_input", 20223751480),
        ],
    )

    # Part 2
    run(
        sum_of_invalid_ids2,
        [
            TestCase("02_example_01", 4174379265),
            TestCase("02_puzzle_input", 30260171216),
        ],
    )
