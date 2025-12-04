from aoc import read_data_as_lines, run, TestCase


def parse(data_file):
    return read_data_as_lines(data_file)


def maximum_joltage(battery_bank: str, allowed_active_batteries: int) -> str:
    total_batteries = len(battery_bank)
    batteries_to_skip = total_batteries - allowed_active_batteries
    battery_chain = []  # Stack of batteries we're turning on

    # while we have batteries_to_skip, turn off weaker batteries
    for battery in battery_bank:
        while battery_chain and batteries_to_skip > 0 and battery_chain[-1] < battery:
            battery_chain.pop()  # Turn off the weaker battery
            batteries_to_skip -= 1
        battery_chain.append(battery)  # Activate this battery

    max_battery_chain = battery_chain[:allowed_active_batteries]
    return "".join(max_battery_chain)


def calculate_max_total_joltage(data_file, allowed_active_batteries):
    battery_banks = parse(data_file)
    return sum(
        int(maximum_joltage(bank, allowed_active_batteries)) for bank in battery_banks
    )


if __name__ == "__main__":
    # Part 1
    run(
        lambda data_file: calculate_max_total_joltage(data_file, 2),
        [
            TestCase("03_example_01", 357),
            TestCase("03_puzzle_input", 17229),
        ],
    )

    # Part 2
    run(
        lambda data_file: calculate_max_total_joltage(data_file, 12),
        [
            TestCase("03_example_01", 3121910778619),
            TestCase("03_puzzle_input", 170520923035051),
        ],
    )
