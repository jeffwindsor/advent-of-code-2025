from aoc import read_data_as_lines, run, TestCase


def parse(data_file):
    return read_data_as_lines(data_file)


def strongest_batteries(battery_bank: str, max_batteries: int) -> int:
    total_batteries = len(battery_bank)
    removals_allowed = total_batteries - max_batteries
    active_batteries = []

    for battery_strength in battery_bank:
        while (
            active_batteries
            and removals_allowed > 0
            and active_batteries[-1] < battery_strength
        ):
            active_batteries.pop()
            removals_allowed -= 1

        active_batteries.append(battery_strength)

    selected_batteries = active_batteries[:max_batteries]
    return int("".join(selected_batteries))


def calculate_total_joltage(data_file, max_batteries):
    battery_banks = parse(data_file)
    return sum(strongest_batteries(bank, max_batteries) for bank in battery_banks)


def calculate_total_joltage_2_batteries(data_file):
    return calculate_total_joltage(data_file, max_batteries=2)


def calculate_total_joltage_12_batteries(data_file):
    return calculate_total_joltage(data_file, max_batteries=12)


if __name__ == "__main__":
    TESTS = [
        TestCase("03_example_01"),
        TestCase("03_puzzle_input"),
    ]

    run(
        calculate_total_joltage_2_batteries,
        TESTS,
        part="part1",
    )
    run(
        calculate_total_joltage_12_batteries,
        TESTS,
        part="part2",
    )
