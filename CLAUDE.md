# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Dependencies

This project uses [aoc-toolkit](https://github.com/jeffwindsor/aoc-toolkit) v1.0.1 for common Advent of Code utilities.

### Installation

```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install git+https://github.com/jeffwindsor/aoc-toolkit.git@v1.0.1
```

### Documentation

Full aoc-toolkit documentation: https://github.com/jeffwindsor/aoc-toolkit

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

def parse(data):
    # Parse input data into usable format
    pass

def part1_solution(data):
    # Solve part 1
    pass

def part2_solution(data):
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

### AOC Toolkit Package

This project uses the external [aoc-toolkit](https://github.com/jeffwindsor/aoc-toolkit) package for reusable utilities. Key modules:

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
- `TestCase(data_file, expected)` - test case definition
- `run(func, test_cases)` - execute tests with colored output
- Displays ✓/✗ with actual vs expected values
- Optional performance metrics (time, memory)

**`aoc.coord`** - Coordinate handling:
- `Coord` - coordinate type/operations
- `filter_coords_in_bounds()` - boundary checking

**`aoc.grid`** - 2D grid operations:
- `Grid` - grid type alias
- Grid size/bounds functions
- Get/set operations
- Find operations (first/all matching positions)
- Direction searching
- Grouping by value
- Visited tracking grids

**`aoc.graph`** - Graph algorithms:
- `bfs()` - breadth-first search
- `dfs()` - depth-first search
- `dfs_grid_path()` - grid path finding
- `dijkstra()` - shortest path
- `find_max_clique()` - clique detection

**`aoc.math`** - Mathematical utilities:
- `count_continuous_segments()` - segment counting
- `count_digits()` - digit counting

**For detailed documentation**, see:
- [Data I/O Guide](https://github.com/jeffwindsor/aoc-toolkit/blob/main/docs/data_io.md)
- [Testing Guide](https://github.com/jeffwindsor/aoc-toolkit/blob/main/docs/testing.md)
- [Coordinates & Grids](https://github.com/jeffwindsor/aoc-toolkit/blob/main/docs/coordinates.md)
- [Algorithms Guide](https://github.com/jeffwindsor/aoc-toolkit/blob/main/docs/algorithms.md)

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
- **Reuse Utilities**: Check [aoc-toolkit](https://github.com/jeffwindsor/aoc-toolkit) before implementing common operations
- **Grid Problems**: Use `aoc.grid` and `aoc.coord` for 2D grid manipulation
- **Graph Problems**: Use `aoc.graph` algorithms (BFS, DFS, Dijkstra)
- **Data Parsing**: Use appropriate `read_data_as_*()` function for input format
