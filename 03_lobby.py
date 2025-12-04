from aoc import read_data_as_lines, run, TestCase


def parse(data_file):
    return read_data_as_lines(data_file)


def select_strongest_batteries(battery_bank: str, max_batteries: int) -> str:
    """
    Select the strongest batteries using a greedy algorithm.

    Strategy: Keep the strongest batteries by removing weaker ones when
    a stronger battery is encountered.

    Args:
        battery_bank: String of battery strengths (digits)
        max_batteries: Maximum number of batteries to keep active

    Returns:
        String representing the strongest battery configuration
    """
    total_batteries = len(battery_bank)
    removals_allowed = total_batteries - max_batteries
    active_batteries = []

    for battery_strength in battery_bank:
        # Remove weaker batteries if we find a stronger one
        while (active_batteries and
               removals_allowed > 0 and
               active_batteries[-1] < battery_strength):
            active_batteries.pop()
            removals_allowed -= 1

        active_batteries.append(battery_strength)

    # Keep only the allowed number of batteries
    selected_batteries = active_batteries[:max_batteries]
    return "".join(selected_batteries)


def calculate_total_joltage(data_file, max_batteries):
    """Calculate total joltage across all battery banks."""
    battery_banks = parse(data_file)
    return sum(
        int(select_strongest_batteries(bank, max_batteries))
        for bank in battery_banks
    )


if __name__ == "__main__":
    # Part 1: Keep 2 batteries per bank
    run(
        lambda data_file: calculate_total_joltage(data_file, max_batteries=2),
        [
            TestCase("03_example_01", 357),
            TestCase("03_puzzle_input", 17229),
        ],
    )

    # Part 2: Keep 12 batteries per bank
    run(
        lambda data_file: calculate_total_joltage(data_file, max_batteries=12),
        [
            TestCase("03_example_01", 3121910778619),
            TestCase("03_puzzle_input", 170520923035051),
        ],
    )
