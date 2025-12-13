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

from aoc import (
    Input,
    run,
    TestCase,
    extract_ints,
    pattern_to_bools,
    calculate_toggle_states,
    extract_bracketed,
    extract_parenthesized,
    extract_braced,
)
from typing import NamedTuple
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

LightStates = list[bool]  # states (on/off) of each light
LightIndices = list[int]  # indices of lights affected by a button
Buttons = list[LightIndices]  # all buttons for a machine


class Machine(NamedTuple):
    buttons: Buttons
    goal: LightStates


def parse_light_pattern(line: str) -> LightStates | None:
    content = extract_bracketed(line)
    return pattern_to_bools(content) if content else None


def parse_buttons(line: str) -> Buttons:
    button_matches = extract_parenthesized(line)
    return [extract_ints(button_str) for button_str in button_matches]


def parse_light_machine(line: str) -> Machine | None:
    goal = parse_light_pattern(line)
    if goal is None:
        return None
    buttons = parse_buttons(line)
    return Machine(buttons, goal)


def parse_light_machines(args: str) -> list[Machine]:
    lines = Input(args).as_lines()
    return [m for m in (parse_light_machine(line) for line in lines) if m is not None]


def apply_button_mask(machine: Machine, mask: int) -> LightStates:
    toggled_lights = [
        light
        for i in range(len(machine.buttons))
        if mask & (1 << i)
        for light in machine.buttons[i]
    ]
    return calculate_toggle_states(toggled_lights, len(machine.goal))


def solve_light_machine(machine: Machine) -> int:
    valid_solutions = (
        bin(mask).count("1")
        for mask in range(1 << len(machine.buttons))
        if apply_button_mask(machine, mask) == machine.goal
    )
    return min(valid_solutions, default=0)


def total_fewest_light_pushes(args: str) -> int:
    return sum(solve_light_machine(machine) for machine in parse_light_machines(args))


JoltageTargets = list[int]


class JoltageMachine(NamedTuple):
    buttons: Buttons
    targets: JoltageTargets


def parse_joltage_targets(line: str) -> JoltageTargets | None:
    content = extract_braced(line)
    return extract_ints(content) if content else None


def parse_joltage_machine(line: str) -> JoltageMachine | None:
    targets = parse_joltage_targets(line)
    if targets is None:
        return None
    buttons = parse_buttons(line)
    return JoltageMachine(buttons, targets)


def parse_joltage_machines(args: str) -> list[JoltageMachine]:
    lines = Input(args).as_lines()
    return [m for m in (parse_joltage_machine(line) for line in lines) if m is not None]


def solve_joltage_machine(machine: JoltageMachine) -> int:
    n_counters = len(machine.targets)
    n_buttons = len(machine.buttons)

    A_eq = np.zeros((n_counters, n_buttons))
    for j, button in enumerate(machine.buttons):
        for counter in button:
            A_eq[counter][j] = 1

    c = np.ones(n_buttons)
    b_eq = np.array(machine.targets, dtype=float)

    constraints = LinearConstraint(A_eq, lb=b_eq, ub=b_eq)
    bounds = Bounds(lb=0, ub=np.inf)
    integrality = np.ones(n_buttons)

    result = milp(c, constraints=constraints, bounds=bounds, integrality=integrality)

    if result.success:
        return int(round(result.fun))
    else:
        raise ValueError("No solution found")


def total_fewest_joltage_pushes(args: str) -> int:
    return sum(solve_joltage_machine(machine) for machine in parse_joltage_machines(args))


if __name__ == "__main__":
    run(
        total_fewest_light_pushes,
        [
            TestCase("data/10_example_01", 7),
            TestCase("data/10_puzzle_input", 425),
        ],
    )

    run(
        total_fewest_joltage_pushes,
        [
            TestCase("data/10_example_01", 33),
            TestCase("data/10_puzzle_input", 15883),
        ],
    )
