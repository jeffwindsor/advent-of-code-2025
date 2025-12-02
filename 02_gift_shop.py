# Problem Analysis:
#   This is a pattern matching and digit manipulation problem. Key CS concepts involved:
#       - String pattern recognition: Detecting if a number follows a specific structure
#       - Modular arithmetic: Working with digit representations
#       - Range iteration: Efficiently checking numbers within bounds
#       - Filtering: Identifying elements that match criteria
#   Key Insights:
#       - Invalid if starts with 0
#       - Invalid ids must have even length
#       - For even length string, paladromes match if string halves match
#       -

from aoc import read_data, run, TestCase


def parse(data_file):
    """
    Parse input file containing comma-separated ranges.

    Args:
        data_file: Name of the data file in ./data/ directory

    Returns:
        List of (start, end) tuples representing ranges

    Example:
        "11-22,95-115" -> [(11, 22), (95, 115)]
    """
    data = read_data(data_file)
    ranges = []
    for range_str in data.split(","):
        start, end = map(int, range_str.strip().split("-"))
        ranges.append((start, end))
    return ranges


def is_invalid_id(n):
    """
    Check if a number is an 'invalid ID'.

    An invalid ID is a number whose digits form a pattern repeated exactly twice.
    Examples: 55 (5 twice), 6464 (64 twice), 123123 (123 twice)

    Args:
        n: Number to check

    Returns:
        True if the number is an invalid ID, False otherwise
    """
    s = str(n)

    # Must have even length to split in half
    if len(s) % 2 != 0:
        return False

    # Split in half and compare
    mid = len(s) // 2
    first_half = s[:mid]
    second_half = s[mid:]

    return first_half == second_half


def sum_of_invalid_ids(data_file):
    """
    Find and sum all invalid IDs in the given ranges.

    Args:
        data_file: Name of the data file containing ranges

    Returns:
        Sum of all invalid IDs found across all ranges
    """
    ranges = parse(data_file)
    total = 0

    for start, end in ranges:
        for num in range(start, end + 1):
            if is_invalid_id(num):
                total += num

    return total


if __name__ == "__main__":
    # Part 1
    run(
        sum_of_invalid_ids,
        [
            TestCase("02_example_01", 1227775554),
            TestCase("02_puzzle_input", 20223751480),
        ],
    )
