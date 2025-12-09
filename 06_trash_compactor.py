from aoc import Input, run, TestCase
from dataclasses import dataclass
from typing import Union
from math import prod


@dataclass
class Add:
    numbers: list[int]


@dataclass
class Multiply:
    numbers: list[int]


Operation = Union[Add, Multiply]


def parse_operation(entry) -> Operation:
    *number_strings, op = entry
    numbers = [int(n) for n in number_strings]
    return Add(numbers) if op == "+" else Multiply(numbers)


def parse(data_file) -> list[Operation]:
    columns = Input.from_file(data_file).as_columns()
    return [parse_operation(col) for col in columns]


def calculate(op: Operation) -> int:
    match op:
        case Add(numbers):
            return sum(numbers)
        case Multiply(numbers):
            return prod(numbers)


def cephalopod_math_homework(data_file):
    ops = parse(data_file)
    values = [calculate(op) for op in ops]
    return sum(values)


if __name__ == "__main__":
    run(
        cephalopod_math_homework,
        [
            TestCase("data/06_example_01", 4277556),
            TestCase("data/06_puzzle_input", 0),
        ],
    )
