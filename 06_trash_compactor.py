from aoc import Input, run, TestCase
from itertools import groupby
from math import prod
from operator import itemgetter

SEPARATOR = " "
SUM_OP = "+"


def parse_and_calculate(entry):
    *number_strings, op = entry
    numbers = [int(n) for n in number_strings]
    return sum(numbers) if op == SUM_OP else prod(numbers)


def parse_with_structure(data_file):
    lines = Input.from_file(data_file, strip_content=False).as_lines()
    max_len = max(len(line) for line in lines)
    return [line.ljust(max_len) for line in lines]


def find_problem_ranges(lines):
    """
    Example:

        Column:  012345678901234
                ┌───────────────┐
        Line 0: |123 328  51 64 |
        Line 1: | 45 64  387 23 |
        Line 2: |  6 98  215 314|
        Line 3: |*   +   *   +  |
                └───────────────┘

        Columns that are all whitespace: 3,7,11
        Making the problem spaces: 0-2, 4-6, 8-10, 12-15

         0 1 2 3 4 5 6 7 8 9 0 1 2 3 4
        ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐
        |1 2 3| |3 2 8| |  5 1| |6 4  |
        |  4 5| |6 4  | |3 8 7| |2 3  |
        |    6| |9 8  | |2 1 5| |3 1 4|
        |*    | |+    | |*    | |+    |
        └─────┘ └─────┘ └─────┘ └─────┘
          P1      P2      P3      P4
    """

    def skip_column(line, col):
        return line[col] == SEPARATOR

    # for columns list of (index:int, is_separator:bool)
    columns = range(len(lines[0]))
    problem_spaces = [
        (col, all(skip_column(line, col) for line in lines)) for col in columns
    ]

    return [
        (idx[0], idx[-1] + 1)
        for skip, problem_space in groupby(problem_spaces, key=itemgetter(1))
        if not skip and (idx := [i for i, _ in problem_space])
    ]


def solve_problem(lines, start, end):
    """
    Example: Problem Space #2 = ["328  ", "64  ", "98  ", "+    "]

    | Column    | Index | Characters      | Digits | Number |
    |-----------|-------|-----------------|--------|--------|
    | Rightmost | 4     | [' ', ' ', ' '] | ""     | Skip   |
    | Next      | 3     | [' ', ' ', ' '] | ""     | Skip   |
    | Next      | 2     | ['8', '4', '8'] | "848"  | 848    |
    | Next      | 1     | ['2', '6', '9'] | "269"  | 269    |
    | Leftmost  | 0     | ['3', ' ', ' '] | "3"    | 3      |

    Operator : "+   ".strip()[0] = "+"
    """
    section = [line[start:end] for line in lines]
    operator = section[-1].strip()[0]

    numbers = [
        int(digit_string)
        for c in range(end - start - 1, -1, -1)
        if (digit_string := "".join(row[c] for row in section[:-1] if row[c].isdigit()))
    ]

    return sum(numbers) if operator == SUM_OP else prod(numbers)


def cephalopod_math_homework(data_file):
    columns = Input.from_file(data_file).as_columns()
    return sum(parse_and_calculate(col) for col in columns)


def cephalopod_math_homework_for_real(data_file):
    lines = parse_with_structure(data_file)
    problems = find_problem_ranges(lines)
    return sum(solve_problem(lines, start, end) for start, end in problems)


if __name__ == "__main__":
    run(
        cephalopod_math_homework,
        [
            TestCase("data/06_example_01", 4277556),
            TestCase("data/06_puzzle_input", 3785892992137),
        ],
    )

    run(
        cephalopod_math_homework_for_real,
        [
            TestCase("data/06_example_01", 3263827),
            TestCase("data/06_puzzle_input", 7669802156452),
        ],
    )
