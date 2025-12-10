from aoc import Input, run, TestCase


def parse(args):
    return Input(args).as_lines()


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


def calculate_total_joltage(args, max_batteries):
    battery_banks = parse(args)
    return sum(strongest_batteries(bank, max_batteries) for bank in battery_banks)


def calculate_total_joltage_2_batteries(args):
    return calculate_total_joltage(args, max_batteries=2)


def calculate_total_joltage_12_batteries(args):
    return calculate_total_joltage(args, max_batteries=12)


if __name__ == "__main__":
    run(
        calculate_total_joltage_2_batteries,
        [
            TestCase("data/03_example_01", 357),
            TestCase("data/03_puzzle_input", 17229),
        ],
    )
    run(
        calculate_total_joltage_12_batteries,
        [
            TestCase("data/03_example_01", 3121910778619),
            TestCase("data/03_puzzle_input", 170520923035051),
        ],
    )
