from aoc import Input, run, TestCase

def parse(args):
    pairs = Input(args).as_key_value_pairs(key_converter=str, value_parser=str.split)
    return dict(pairs)

def count_paths(graph, current, target, visited):
    if current == target:
        return 1

    if current in visited or current not in graph:
        return 0

    visited.add(current)
    total = sum(count_paths(graph, neighbor, target, visited)
                for neighbor in graph[current])
    visited.remove(current)
    return total

def count_all_paths_out(args):
    graph = parse(args)
    return count_paths(graph, "you", "out", set())

if __name__ == "__main__":
    run(count_all_paths_out, [
        TestCase("data/11_example_01", 5),
        TestCase("data/11_puzzle_input", 555),
    ])
