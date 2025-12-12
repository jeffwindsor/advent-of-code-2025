"""
Problem Restatement

Given:
- Machines with N indicator lights (all initially OFF)
- Target pattern: which lights should be ON/OFF
- Buttons: each toggles a specific set of lights
- Pressing a button multiple times: toggle states repeatedly

Find: Minimum total button presses across all machines to reach target states

Key Insights

1. XOR/Toggle Math (GF(2) arithmetic):
  - Pressing a button twice = no effect (toggle twice returns to original)
  - Therefore: we only care about pressing each button 0 or 1 times
  - This reduces problem from "how many times to press" to "which buttons to press"
2. Linear Algebra over Binary Field:
  - Each button is a binary vector (which lights it affects)
  - Current state XOR button effects = target state
  - This is a system of linear equations over GF(2) (mod 2)
3. Optimization Goal:
  - Among all valid button combinations, find the one with minimum weight (fewest buttons pressed)

"""

from aoc import Input, run, TestCase, extract_ints
import re
from typing import NamedTuple
from collections import Counter
import numpy as np
from scipy.optimize import linprog

LightStates = list[bool]  # states (on/off) of each light
LightIndices = list[int]  # indices of lights affected by a button
Buttons = list[LightIndices]  # all buttons for a machine


class Machine(NamedTuple):
    buttons: Buttons
    goal: LightStates


def parse_goal(line: str) -> LightStates | None:
    target_match = re.search(r"\[([.#]+)\]", line)
    return [c == "#" for c in target_match.group(1)] if target_match else None


def parse_buttons(line: str) -> Buttons:
    button_matches = re.findall(r"\(([0-9,]+)\)", line)
    return [extract_ints(button_str) for button_str in button_matches]


def parse_machine(line: str) -> Machine | None:
    goal = parse_goal(line)
    if goal is None:
        return None
    buttons = parse_buttons(line)
    return Machine(buttons, goal)


def parse(args: str) -> list[Machine]:
    lines = Input(args).as_lines()
    return [m for m in (parse_machine(line) for line in lines) if m is not None]


def apply_button_mask(machine: Machine, mask: int) -> LightStates:
    toggled_lights = [
        light
        for i in range(len(machine.buttons))
        if mask & (1 << i)
        for light in machine.buttons[i]
    ]
    # collects toogle count per light, toggled_lights of [1, 3, 2, 3] gives Counter({1: 1, 2: 1, 3: 2})
    toggle_counts = Counter(toggled_lights)
    # a light is on if toggled an odd number of times
    return [toggle_counts.get(i, 0) % 2 == 1 for i in range(len(machine.goal))]


def fewest_pushes_to_goal(machine: Machine) -> int:
    valid_solutions = (
        bin(mask).count("1")
        for mask in range(1 << len(machine.buttons))
        if apply_button_mask(machine, mask) == machine.goal
    )
    return min(valid_solutions, default=0)


def total_fewest_pushes_to_goal(args: str) -> int:
    return sum(fewest_pushes_to_goal(machine) for machine in parse(args))


if __name__ == "__main__":
    run(
        total_fewest_pushes_to_goal,
        [
            TestCase("data/10_example_01", 7),
            TestCase("data/10_puzzle_input", 425),
        ],
    )
