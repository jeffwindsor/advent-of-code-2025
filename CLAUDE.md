# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Running Solutions
- **Run all solutions**: `./run`
- **Run specific day**: `./run N` (e.g., `./run 1` runs `01_*.py`)
- **Run single solution directly**: `python3 01_secret_entrance.py`

### Performance Metrics
- **Configuration file**: `.aoc_config`
- **Enable performance tracking**: Add `test_performance_tracking=true` to `.aoc_config`
- **Disable performance tracking**: Set `test_performance_tracking=false` or delete `.aoc_config`
- When enabled, displays execution time and memory usage for each test case
- Quick commands:
  - Enable: `echo "test_performance_tracking=true" > .aoc_config`
  - Disable: `echo "test_performance_tracking=false" > .aoc_config` or `rm .aoc_config`

## Project Architecture

### Solution Structure Pattern
Each daily puzzle follows this structure:
```python
from aoc import read_data_as_lines, run, TestCase

def parse(args):
    # Parse input data into usable format
    pass

def part1_solution(args):
    # Solve part 1
    pass

def part2_solution(args):
    # Solve part 2
    pass

if __name__ == "__main__":
    # Part 1 tests
    run(part1_solution, [
        TestCase("NN_example_01", expected_value),
        TestCase("NN_puzzle_input", expected_value),
    ])

    # Part 2 tests
    run(part2_solution, [
        TestCase("NN_example_01", expected_value),
        TestCase("NN_puzzle_input", expected_value),
    ])
```

### Multi-Argument Functions

When solution functions need additional parameters beyond the data file:

```python
def solve(args, num_iterations):
    coords = parse(args)
    # ... implementation

run(solve, [
    TestCase(["data/08_example_01", 10], expected=40),
    TestCase(["data/08_puzzle_input", 1000], expected=131150),
])
```

### AOC Package

This project uses the local `aoc` package for reusable utilities. Key modules:

**`aoc.data`** - Data I/O utilities:
- `read_data()` - raw text
- `read_data_as_lines()` - list of strings
- `read_data_as_ints()` - list of integers
- `read_data_as_char_grid()` - 2D character grid
- `read_data_as_int_grid()` - 2D integer grid
- `read_data_as_coord_pairs()` - coordinate pairs
- `read_data_as_graph_edges()` - graph edge lists
- `read_data_as_sections()` - multi-section data
- `read_data_as_columns()` - columnar data
- `extract_ints()` - extract integers from text

**`aoc.testing`** - Test framework:
- `TestCase(args, expected)` - test case definition (args can be a string or list of arguments)
- `run(func, test_cases)` - execute tests with colored output
- Displays ✓/✗ with actual vs expected values
- Optional performance metrics (time, memory)

**`aoc.d2`** - 2D coordinate and grid operations:
- `Coord(row, col)` - immutable 2D coordinate
- `Dimension(width, height)` - 2D grid dimensions
- `Grid` - 2D grid wrapper with coordinate-based access
- Direction constants: `ZERO`, `UP`, `DOWN`, `LEFT`, `RIGHT`, `UP_LEFT`, etc.
- Direction collections: `DIRECTIONS_CARDINAL`, `DIRECTIONS_INTERCARDINAL`, `DIRECTIONS_ALL`
- Coord methods: `__add__`, `__sub__`, `in_bounds`, `manhattan_distance`, `neighbors`
- Grid methods: `coords`, `find_first`, `find_all`, `group_by_value`, `search_in_direction`, `create`
- `filter_coords_in_bounds()` - filter coordinates within bounds

**`aoc.d3`** - 3D coordinate and grid operations:
- `Coord(x, y, z)` - immutable 3D coordinate
- `Dimension(width, height, depth)` - 3D grid dimensions
- `Grid` - 3D grid wrapper with coordinate-based access
- Direction constants: `ZERO`, `UP`, `DOWN`, `LEFT`, `RIGHT`, `FORWARD`, `BACK`
- Direction collection: `DIRECTIONS_CARDINAL` (6 directions)
- Coord methods: `__add__`, `__sub__`, `in_bounds`, `manhattan_distance`, `neighbors`
- Grid methods: `coords`, `find_first`, `find_all`, `group_by_value`, `create`
- `filter_coords_in_bounds()` - filter coordinates within bounds
- Note: Requires explicit import: `from aoc.d3 import Coord, Grid`

**`aoc.graph`** - Graph algorithms:
- `bfs()` - breadth-first search
- `dfs()` - depth-first search
- `dfs_grid_path()` - grid path finding
- `dijkstra()` - shortest path
- `find_max_clique()` - clique detection

**`aoc.math`** - Mathematical utilities:
- `count_continuous_segments()` - segment counting
- `count_digits()` - digit counting

### Data File Conventions
- Location: `data/` directory
- Naming: `{day}_{type}` (zero-padded day number)
  - Example data: `01_example_01`, `02_example_01`
  - Puzzle input: `01_puzzle_input`, `02_puzzle_input`
- Puzzle inputs are gitignored (`data/*puzzle_input*`)

### Solution File Conventions
- Naming: `{day}_{description}.py` (e.g., `01_secret_entrance.py`)
- Always include both example and puzzle input test cases
- Expected values stored in `.answer` files (see Answer File Pattern below)

### Answer File Pattern (PREFERRED)
Expected test answers are stored in separate `.{part}.answer` files alongside data files:

**File Structure:**
```
data/04_example_01                # Test input data
data/04_example_01.part1.answer   # Part 1 expected answer
data/04_example_01.part2.answer   # Part 2 expected answer
data/04_puzzle_input              # Puzzle input (gitignored)
data/04_puzzle_input.part1.answer # Part 1 answer (gitignored)
data/04_puzzle_input.part2.answer # Part 2 answer (gitignored)
```

**Usage in Solution Files:**
```python
if __name__ == "__main__":
    TESTS = [
        TestCase("04_example_01"),
        TestCase("04_puzzle_input"),
    ]

    run(part1_solution, TESTS, part="part1")
    run(part2_solution, TESTS, part="part2")
```

**Override with explicit expected value when needed:**
```python
TESTS = [
    TestCase("04_example_01", 13),  # explicit value overrides answer file
    TestCase("04_puzzle_input"),    # loads from answer file
]

run(part1_solution, TESTS, part="part1")
```

**Benefits:**
- Clean script files without hardcoded expected values
- Easy to update answers without touching code
- Answers naturally gitignored alongside puzzle inputs
- Explicit test case list shows what's being tested
- Explicit part specification prevents confusion
- Can override with explicit `TestCase("file", expected_value)` when needed

## Development Workflow

1. Create new solution file: `NN_puzzle_name.py`
2. Create corresponding data files in `data/`:
   - `NN_example_01` (example from problem statement)
   - `NN_puzzle_input` (actual puzzle input)
3. Import utilities from `aoc` package as needed
4. Implement parse, part1, and part2 functions
5. Add test cases with expected values
6. Run with `./run NN` to verify
7. Enable performance metrics with `echo "test_performance_tracking=true" > .aoc_config` if optimizing

## Code Style Preferences

- **No Docstrings**: Do not add docstrings to functions
- **No Comments**: Do not add comments unless absolutely critical for understanding
- **Self-Documenting Code**: Use clear function and variable names instead

## Key Patterns

- **Separation of Concerns**: Parse once, solve multiple parts
- **Test-Driven**: Include test cases with expected values from the start
- **Reuse Utilities**: Use `aoc` package utilities before implementing common operations
- **2D Grid Problems**: Use `aoc.d2` (Coord, Grid) for 2D spatial manipulation
- **3D Grid Problems**: Use `aoc.d3` (Coord, Grid) for 3D spatial manipulation
- **Graph Problems**: Use `aoc.graph` algorithms (BFS, DFS, Dijkstra)
- **Data Parsing**: Use appropriate `read_data_as_*()` function for input format
