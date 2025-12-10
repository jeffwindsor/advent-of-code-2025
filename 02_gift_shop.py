from aoc import Input, run, TestCase


def parse(args):
    ranges = Input(args).content.split(",")
    return [tuple(int(x) for x in r.split("-")) for r in ranges]


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


def sum_matching_numbers(args, predicate):
    ranges = parse(args)
    return sum(
        number
        for start, end in ranges
        for number in range(start, end + 1)
        if predicate(number)
    )


def sum_of_invalid_ids1(args):
    return sum_matching_numbers(args, has_pattern_repeated_exactly_twice)


def sum_of_invalid_ids2(args):
    return sum_matching_numbers(args, has_repeating_pattern)


if __name__ == "__main__":
    run(
        sum_of_invalid_ids1,
        [
            TestCase("data/02_example_01", 1227775554),
            TestCase("data/02_puzzle_input", 20223751480),
        ],
    )
    run(
        sum_of_invalid_ids2,
        [
            TestCase("data/02_example_01", 4174379265),
            TestCase("data/02_puzzle_input", 30260171216),
        ],
    )
