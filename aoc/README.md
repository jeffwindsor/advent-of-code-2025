# AOC Utilities

Reusable utilities for Advent of Code puzzles.

## Requirements

- Python 3.10 or higher

## Quick Start

```python
# Flat imports (recommended) - defaults to 2D
from aoc import Input, Grid, Coord, Dimension, bfs, dijkstra, run, TestCase

# Explicit 2D imports
from aoc.d2 import Coord, Grid, Dimension

# Explicit 3D imports
from aoc.d3 import Coord, Grid, Dimension

# Other modules
from aoc.input import Input
from aoc.graph import bfs, dijkstra
from aoc.testing import run, TestCase
```

## API Reference

### Input - Parse AOC puzzle inputs

Flexible parser for common AOC input patterns. Create from file or string, then chain parsing methods.

```python
# From file
input = Input("data/puzzle.txt")

# From string
input = Input.from_string("1,2,3\n4,5,6")

# Preserve whitespace (useful for structured spacing)
input = Input.from_file("data/puzzle.txt", strip_content=False)
```

**Lines & Sections**
```python
input.as_lines()                    # ["line1", "line2", "line3"]
input.as_sections()                 # Split on blank lines → [Input, Input, ...]
rules, updates = input.as_sections()  # Unpack two sections
```

**Grids**
```python
input.as_grid()                     # Grid of characters
input.as_int_grid()                 # Grid of digit ints (non-digits → -1)
input.as_grid(str.upper)            # Grid with converter function
```

**Coordinates**
```python
input.as_coords()                   # "6,1\n8,3" → [Coord(6,1), Coord(8,3)]
input.as_coords(separator=",")     # Custom separator
```

**Delimited Values**
```python
input.as_delimited_lines()          # "1,2,3\n4,5,6" → [[1,2,3], [4,5,6]]
input.as_delimited_lines(";", str)  # Custom separator and type
input.as_columns()                  # "1 2\n3 4" → [('1','3'), ('2','4')]
input.as_columns(converter=int)     # "1 2\n3 4" → [(1,3), (2,4)]
```

**Key-Value Pairs**
```python
input.as_key_value_pairs()          # "190: 10 19" → [(190, [10,19])]
input.as_key_value_pairs(str, str.split)  # Custom parsers
```

**Graph Edges**
```python
input.as_adjacency_list()           # "A-B\nB-C" → {'A':{'B'}, 'B':{'A','C'}, ...}
input.as_adjacency_list("-", directed=True)  # Directional edges
```

**Raw Access**
```python
input.content                       # Raw string content
extract_ints(text)                  # Extract all integers from text
extract_pattern(text, r"\d+")       # Extract regex matches
```

**Whitespace Control**
```python
# Default: strips whitespace from file and lines
Input.from_file("data.txt").as_lines()
# → ['line1', 'line2']  (leading/trailing spaces removed)

# Preserve structural spacing (e.g., column-aligned data)
Input.from_file("data.txt", strip_content=False).as_lines(skip_empty=False)
# → ['  line1  ', ' line2 ', '']  (preserves spaces and empty lines)
```

### d2 - 2D Coordinates and Grids

**Coord** - Immutable 2D coordinates with direction support

```python
coord = Coord(row=5, col=3)
coord = Coord(5, 3)                 # Row-major order

# Arithmetic
coord + Coord.RIGHT                 # Coord(5, 4)
coord - other                       # Vector subtraction
coord.manhattan_distance(other)     # |Δrow| + |Δcol|

# Bounds checking
coord.in_bounds(Coord(10, 10))      # Within (0,0) to (10,10)
coord.neighbors(max_bounds)         # Cardinal neighbors in bounds
coord.neighbors(max_bounds, Coord.DIRECTIONS_ALL)  # All 8 directions

# Direction constants
Coord.ZERO                          # Coord(0, 0)
Coord.UP, DOWN, LEFT, RIGHT         # Cardinal: (-1,0), (1,0), (0,-1), (0,1)
Coord.UP_LEFT, UP_RIGHT             # Intercardinal diagonals
Coord.DOWN_LEFT, DOWN_RIGHT

# Direction sets
Coord.DIRECTIONS_CARDINAL           # [UP, RIGHT, DOWN, LEFT]
Coord.DIRECTIONS_INTERCARDINAL      # [UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT]
Coord.DIRECTIONS_ALL                # All 8 directions

# Rotation
Coord.TURN_CLOCKWISE[direction]     # Rotate direction 90° CW
Coord.TURN_COUNTER_CLOCKWISE[dir]   # Rotate direction 90° CCW
```

**Grid** - 2D array with coordinate access

```python
grid = Grid([['#', '.', '#'],
             ['.', '.', '.'],
             ['#', '.', '#']])

# Access by coordinate
grid[Coord(0, 1)]                   # '.'
grid[coord] = 'X'                   # Set value
coord in grid                       # Check bounds

# Properties
grid.size                           # Dimension(width=3, height=3)
grid.max_bounds                     # Coord(col=2, row=2)

# Search
grid.find_first('.')                # First coord with value
grid.find_all('.')                  # All coords with value
grid.group_by_value(exclude='#')    # {'.': [coord1, coord2, ...]}

# Iteration
for coord, value in grid.coords():
    print(coord, value)

# Direction search
grid.search_in_direction(start, Coord.RIGHT, "XMAS")  # True if found

# Creation
Grid.create(Dimension(10, 10), '.')  # 10x10 grid filled with '.'
```

**Dimension** - 2D grid size representation

```python
size = Dimension(width=10, height=5)  # 10 cols, 5 rows
```

**Utilities**

```python
# Filter coordinates within bounds
filter_coords_in_bounds(coords, max_bounds)
filter_coords_in_bounds(coords, max_bounds, min_bounds)
```

### d3 - 3D Coordinates and Grids

**Coord** - Immutable 3D coordinates with direction support

```python
from aoc.d3 import Coord, Grid, Dimension

coord = Coord(x=5, y=3, z=2)

# Arithmetic
coord + Coord.RIGHT                 # Coord(6, 3, 2)
coord - other                       # Vector subtraction
coord.manhattan_distance(other)     # |Δx| + |Δy| + |Δz|

# Bounds checking
coord.in_bounds(Coord(10, 10, 10))  # Within (0,0,0) to (10,10,10)
coord.neighbors(max_bounds)          # Cardinal neighbors in bounds

# Direction constants (6 cardinal directions)
Coord.ZERO                          # Coord(0, 0, 0)
Coord.UP, DOWN                      # (0, 1, 0), (0, -1, 0)
Coord.LEFT, RIGHT                   # (-1, 0, 0), (1, 0, 0)
Coord.FORWARD, BACK                 # (0, 0, 1), (0, 0, -1)

# Direction set
Coord.DIRECTIONS_CARDINAL           # All 6 cardinal directions
```

**Grid** - 3D array with coordinate access

```python
from aoc.d3 import Grid, Dimension

# Create 3D grid
grid = Grid.create(Dimension(10, 10, 10), '.')

# Access by coordinate
grid[Coord(5, 3, 2)]                # Get value
grid[coord] = 'X'                   # Set value
coord in grid                       # Check bounds

# Properties
grid.size                           # Dimension(width=10, height=10, depth=10)
grid.max_bounds                     # Coord(x=9, y=9, z=9)

# Search
grid.find_first('X')                # First coord with value
grid.find_all('X')                  # All coords with value
grid.group_by_value(exclude='.')    # {'X': [coord1, coord2, ...]}

# Iteration
for coord, value in grid.coords():
    print(coord, value)
```

**Dimension** - 3D grid size representation

```python
size = Dimension(width=10, height=5, depth=8)  # 10×5×8
```

**Utilities**

```python
# Filter coordinates within bounds
filter_coords_in_bounds(coords, max_bounds)
filter_coords_in_bounds(coords, max_bounds, min_bounds)
```

### Graph - Search algorithms

Generic graph search algorithms that work with any hashable state.

**BFS - Breadth-first search**
```python
# Find all distances
distances = bfs(start, neighbors_func)           # {state: distance, ...}

# Find path to goal
path = bfs(start, neighbors_func, goal_func)     # [state1, state2, ...]

# Grid pathfinding (shortest path)
path = bfs_grid_path(grid, start, end, {'.', 'O'})  # walkable values
```

**DFS - Depth-first search**
```python
# Find any path to goal (not shortest)
path = dfs(start, neighbors_func, goal_func)     # [state1, state2, ...]

# Grid pathfinding
path = dfs_grid_path(grid, start, end, {'.', 'O'})
```

**Dijkstra - Weighted shortest path**
```python
def neighbors_func(coord):
    return [(neighbor, cost), ...]  # List of (state, cost) tuples

distances = dijkstra(start, neighbors_func)       # {state: min_cost, ...}
distances = dijkstra(start, neighbors_func, goal) # Early exit at goal
```

**Max Clique - Find largest fully-connected subgraph**
```python
graph = {'A': {'B', 'C'}, 'B': {'A', 'C'}, 'C': {'A', 'B'}}
clique = find_max_clique(graph)                  # {'A', 'B', 'C'}
```

**Neighbor function pattern**
```python
# Simple neighbor function
def neighbors(coord):
    return [coord + d for d in Coord.DIRECTIONS_CARDINAL
            if (coord + d) in grid and grid[coord + d] != '#']

# Weighted neighbor function
def weighted_neighbors(coord):
    return [(coord + d, grid[coord + d])
            for d in Coord.DIRECTIONS_CARDINAL if (coord + d) in grid]

# State-based (for complex problems)
def state_neighbors(state):
    coord, direction = state
    return [((coord + direction, direction), 1),           # Move forward
            ((coord, turn_clockwise[direction]), 1000)]    # Turn
```

### Math - Mathematical utilities

```python
count_continuous_segments(data)     # Count continuous non-zero segments
count_digits(number)                # Count digits in integer
```

### Testing - Test framework with colored output

Simple test framework for validating puzzle solutions.

```python
from aoc import run, TestCase

def solve(args):
    data = Input(args).as_lines()
    return len(data)

# Single argument (file path)
run(solve, [
    TestCase("data/01_example_01", expected=10),
    TestCase("data/01_puzzle_input", expected=200),
])
```

**Multi-argument functions**

When your solution needs additional parameters:

```python
def solve(args, iterations):
    data = Input(args).as_lines()
    # ... process with iterations

# Pass multiple arguments as a list
run(solve, [
    TestCase(["data/08_example_01", 10], expected=40),
    TestCase(["data/08_puzzle_input", 1000], expected=131150),
])
```

**Answer Files**

Store expected answers in `.part1.answer` and `.part2.answer` files:

```python
# Test cases without explicit expected values
run(part1_solution, [
    TestCase("data/04_example_01"),
    TestCase("data/04_puzzle_input"),
], part="part1")

run(part2_solution, [
    TestCase("data/04_example_01"),
    TestCase("data/04_puzzle_input"),
], part="part2")
```

**Features**
- Colored output: Green ✓ for pass, Red ✗ for fail
- Shows actual vs expected values on mismatch
- Optional performance metrics (time, memory) via config file
- Summary line showing pass/fail count

**Performance Tracking**

Create `.aoc_config` file:

```bash
# Enable performance metrics
echo "test_performance_tracking=true" > .aoc_config

# Disable performance metrics
echo "test_performance_tracking=false" > .aoc_config
# or
rm .aoc_config
```

## Module Structure

```
aoc/
├── d2.py           # 2D coordinates and grids
├── d3.py           # 3D coordinates and grids
├── graph.py        # Search algorithms (BFS, DFS, Dijkstra, max clique)
├── input.py        # Data reading and parsing
├── math.py         # Mathematical utilities
└── testing.py      # Test framework
```

## License

CC BY-NC-SA 4.0
