"""Testing utilities for Advent of Code puzzles."""

import os
import inspect
import time
import tracemalloc
from dataclasses import dataclass
from typing import Callable, Any


# ========== Configuration ==========
def _is_perf_enabled() -> bool:
    config_file = ".aoc_config"
    if os.path.exists(config_file):
        try:
            with open(config_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("test_performance_tracking="):
                        value = line.split("=", 1)[1].strip().lower()
                        return value in ("true", "1", "yes")
        except Exception:
            pass
    return False


# Cache at module load time for zero per-test overhead
PERF_ENABLED = _is_perf_enabled()


# ========== Colors ==========

TITLE_COLOR = "\033[34m"
FALSE_COLOR = "\033[91m"
TRUE_COLOR = "\033[92m"
END_COLOR = "\033[0m"


# ========== Formatting ==========


def format_time(seconds: float) -> str:
    if seconds < 0.001:
        return f"{seconds * 1_000_000:.0f}µs"
    elif seconds < 1.0:
        return f"{seconds * 1000:.2f}ms"
    else:
        return f"{seconds:.2f}s"


def format_memory(bytes_used: int) -> str:
    if bytes_used < 1024:
        return f"{bytes_used}B"
    elif bytes_used < 1024 * 1024:
        return f"{bytes_used / 1024:.1f}KB"
    else:
        return f"{bytes_used / (1024 * 1024):.1f}MB"


# ========== Test Framework ==========


@dataclass
class TestCase:
    data_file: str
    expected: Any


def run(func: Callable[[str], Any], test_cases: list[TestCase]) -> None:
    """
    Execute test cases for a given function and report results with performance metrics.
    """

    filename = os.path.basename(inspect.stack()[1].filename)
    print(f"{TITLE_COLOR}{func.__name__}{END_COLOR}")

    passed = 0
    failed = 0

    for test_case in test_cases:
        try:
            # Start performance tracking (if enabled)
            if PERF_ENABLED:
                tracemalloc.start()
                start_time = time.perf_counter()

            # Execute test
            actual = func(test_case.data_file)

            # Capture and format metrics (if enabled)
            if PERF_ENABLED:
                elapsed_time = time.perf_counter() - start_time
                current_mem, peak_mem = tracemalloc.get_traced_memory()
                tracemalloc.stop()

                time_str = format_time(elapsed_time)
                mem_str = format_memory(peak_mem)
                metrics = f" ({time_str}, {mem_str})"
            else:
                metrics = ""

            # Report results
            if test_case.expected == actual:
                print(
                    f"  {test_case.data_file}: {TRUE_COLOR}{actual}{metrics}{END_COLOR}"
                )
                passed += 1
            else:
                print(
                    f"  {test_case.data_file}: {FALSE_COLOR}Expected {test_case.expected} but actual is {actual}{metrics}{END_COLOR}"
                )
                failed += 1
        except Exception as e:
            # Stop tracking on error (if enabled)
            if PERF_ENABLED and tracemalloc.is_tracing():
                tracemalloc.stop()
            print(
                f"  {test_case.data_file}: {FALSE_COLOR}ERROR: {type(e).__name__}: {e}{END_COLOR}"
            )
            failed += 1

    # Print summary
    total = passed + failed
    summary_color = TRUE_COLOR if failed == 0 else FALSE_COLOR
    print(f"{summary_color}  {passed}/{total} tests passed{END_COLOR}")
    print()


__all__ = [
    "TestCase",
    "run",
    "PERF_ENABLED",
    "format_time",
    "format_memory",
]
