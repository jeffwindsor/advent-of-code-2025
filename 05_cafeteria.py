from aoc import Input, run, TestCase


def parse(data_file):
    ranges_section, ids_section = Input(data_file).as_sections()
    ranges = [tuple(int(x) for x in line.split("-")) for line in ranges_section.as_lines()]
    ids = [int(line) for line in ids_section.as_lines()]
    return ranges, ids


def is_fresh(ingredient_id, ranges):
    return any(start <= ingredient_id <= end for start, end in ranges)


def ranges_touch_or_overlap(start, last_end):
    return start - last_end <= 1


def merge_ranges(ranges):
    if not ranges:
        return []

    sorted_ranges = sorted(ranges, key=lambda r: r[0])
    merged = [sorted_ranges[0]]

    for start, end in sorted_ranges[1:]:
        last_start, last_end = merged[-1]

        if ranges_touch_or_overlap(start, last_end):
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))

    return merged


def count_fresh_ingredients(data_file):
    ranges, ids = parse(data_file)
    return sum(1 for ingredient_id in ids if is_fresh(ingredient_id, ranges))


def count_total_fresh_ids(data_file):
    ranges_section, _ = Input(data_file).as_sections()
    ranges = [tuple(int(x) for x in line.split("-")) for line in ranges_section.as_lines()]
    merged = merge_ranges(ranges)
    return sum(end - start + 1 for start, end in merged)


if __name__ == "__main__":
    run(
        count_fresh_ingredients,
        [
            TestCase("data/05_example_01", 3),
            TestCase("data/05_puzzle_input", 674),
        ],
    )
    run(
        count_total_fresh_ids,
        [
            TestCase("data/05_example_01", 14),
            TestCase("data/05_puzzle_input", 352509891817881),
        ],
    )
