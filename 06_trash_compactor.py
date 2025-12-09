from aoc import Input, run, TestCase
from math import prod


def parse_and_calculate(entry):
    *number_strings, op = entry
    numbers = [int(n) for n in number_strings]
    return sum(numbers) if op == "+" else prod(numbers)


def cephalopod_math_homework(data_file):
    columns = Input.from_file(data_file).as_columns()
    return sum(parse_and_calculate(col) for col in columns)


if __name__ == "__main__":
    run(
        cephalopod_math_homework,
        [
            TestCase("data/06_example_01", 4277556),
            TestCase("data/06_puzzle_input", 3785892992137),
        ],
    )
