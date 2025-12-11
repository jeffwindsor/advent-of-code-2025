from aoc import Input, run, TestCase
from typing import NamedTuple


class Range(NamedTuple):
    start: int
    end: int


def parse(args):
    ranges_section, ids_section = Input(args).as_sections()
    ranges = [Range(*map(int, line.split("-"))) for line in ranges_section.as_lines()]
    ids = [int(line) for line in ids_section.as_lines()]
    return ranges, ids


def is_fresh(ingredient_id, ranges):
    return any(r.start <= ingredient_id <= r.end for r in ranges)


def ranges_touch_or_overlap(start, last_end):
    return start - last_end <= 1


def merge_ranges(ranges):
    if not ranges:
        return []

    sorted_ranges = sorted(ranges, key=lambda r: r.start)
    merged = [sorted_ranges[0]]

    for r in sorted_ranges[1:]:
        last = merged[-1]

        if ranges_touch_or_overlap(r.start, last.end):
            merged[-1] = Range(last.start, max(last.end, r.end))
        else:
            merged.append(r)

    return merged


def count_fresh_ingredients(args):
    ranges, ids = parse(args)
    return sum(1 for ingredient_id in ids if is_fresh(ingredient_id, ranges))


def count_total_fresh_ids(args):
    ranges_section, _ = Input(args).as_sections()
    ranges = [Range(*map(int, line.split("-"))) for line in ranges_section.as_lines()]
    merged = merge_ranges(ranges)
    return sum(r.end - r.start + 1 for r in merged)


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
