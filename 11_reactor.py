from aoc import Input, run, TestCase
from aoc.graph import count_paths_dag


def parse(args):
    pairs = Input(args).as_key_value_pairs(key_converter=str, value_parser=str.split)
    return dict(pairs)


def count_paths(graph, current, target, visited):
    if current == target:
        return 1

    if current in visited or current not in graph:
        return 0

    visited.add(current)
    total = sum(
        count_paths(graph, neighbor, target, visited) for neighbor in graph[current]
    )
    visited.remove(current)
    return total


def count_all_paths_out(args):
    graph = parse(args)
    return count_paths(graph, "you", "out", set())


def count_paths_visiting_dac_and_fft(args):
    graph = parse(args)

    def neighbors(node):
        return graph.get(node, [])

    # Multiplicative counting: svr → fft → dac → out
    paths_fft_then_dac = (
        count_paths_dag("svr", "fft", neighbors)
        * count_paths_dag("fft", "dac", neighbors)
        * count_paths_dag("dac", "out", neighbors)
    )

    # Multiplicative counting: svr → dac → fft → out
    paths_dac_then_fft = (
        count_paths_dag("svr", "dac", neighbors)
        * count_paths_dag("dac", "fft", neighbors)
        * count_paths_dag("fft", "out", neighbors)
    )

    return paths_fft_then_dac + paths_dac_then_fft


if __name__ == "__main__":
    run(
        count_all_paths_out,
        [
            TestCase("data/11_example_01", 5),
            TestCase("data/11_puzzle_input", 555),
        ],
    )

    run(
        count_paths_visiting_dac_and_fft,
        [
            TestCase("data/11_example_02", 2),
            TestCase("data/11_puzzle_input", 502447498690860),
        ],
    )
