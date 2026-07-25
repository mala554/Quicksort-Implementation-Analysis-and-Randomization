"""
empirical_analysis.py

Benchmarks deterministic and randomized Quicksort on random, sorted,
and reverse-sorted inputs across several input sizes. Increases
Python's recursion limit to accommodate the worst-case O(n) recursion
depth of the deterministic version on already-sorted input. Writes
results to results/timings.csv and a plot to results/timings.png.

Author: Kelvin
Assignment 5: Quicksort Algorithm: Implementation, Analysis, and Randomization
"""

import csv
import random
import sys
import time

sys.setrecursionlimit(20000)

from quicksort import quicksort, randomized_quicksort  # noqa: E402

SIZES = [100, 500, 1000, 2000, 4000, 6000]
DISTRIBUTIONS = ["random", "sorted", "reverse_sorted"]
TRIALS = 5  # repeated runs per configuration, timings are averaged


def make_input(size, distribution):
    """Build a list of the given size and distribution."""
    if distribution == "random":
        return [random.randint(0, 1_000_000) for _ in range(size)]
    elif distribution == "sorted":
        return list(range(size))
    elif distribution == "reverse_sorted":
        return list(range(size, 0, -1))
    raise ValueError(f"Unknown distribution: {distribution}")


def time_sort(sort_fn, data):
    """Time a single sort call on a copy of data. Returns seconds."""
    arr = data.copy()
    start = time.perf_counter()
    sort_fn(arr)
    end = time.perf_counter()
    assert arr == sorted(data), "Sort produced an incorrect result"
    return end - start


def run_benchmarks():
    rows = []
    for distribution in DISTRIBUTIONS:
        for size in SIZES:
            det_times = []
            rand_times = []
            for _ in range(TRIALS):
                data = make_input(size, distribution)

                # Deterministic quicksort on sorted/reverse-sorted data
                # with the last-element pivot degrades to O(n^2)
                # recursion depth. Skip sizes that would blow the
                # recursion limit or take too long, and note it.
                try:
                    det_times.append(time_sort(quicksort, data))
                except RecursionError:
                    det_times.append(None)

                rand_times.append(time_sort(randomized_quicksort, data))

            valid_det = [t for t in det_times if t is not None]
            avg_det = sum(valid_det) / len(valid_det) if valid_det else None
            avg_rand = sum(rand_times) / len(rand_times)

            rows.append({
                "distribution": distribution,
                "size": size,
                "deterministic_avg_sec": avg_det,
                "randomized_avg_sec": avg_rand,
            })
            det_display = f"{avg_det:.6f}" if avg_det is not None else "RecursionError"
            print(f"{distribution:15s} n={size:5d}  "
                  f"deterministic={det_display:>12}  "
                  f"randomized={avg_rand:.6f}")
    return rows


def write_csv(rows, path):
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "distribution", "size", "deterministic_avg_sec", "randomized_avg_sec"
        ])
        writer.writeheader()
        writer.writerows(rows)


def plot_results(rows, path):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not available, skipping plot generation.")
        return

    fig, axes = plt.subplots(1, len(DISTRIBUTIONS), figsize=(15, 4.5), sharey=False)

    for ax, distribution in zip(axes, DISTRIBUTIONS):
        subset = [r for r in rows if r["distribution"] == distribution]
        sizes = [r["size"] for r in subset]
        det = [r["deterministic_avg_sec"] for r in subset]
        rand = [r["randomized_avg_sec"] for r in subset]

        if any(d is not None for d in det):
            det_sizes = [s for s, d in zip(sizes, det) if d is not None]
            det_vals = [d for d in det if d is not None]
            ax.plot(det_sizes, det_vals, marker="o", label="Deterministic")
        ax.plot(sizes, rand, marker="o", label="Randomized")
        ax.set_title(distribution.replace("_", " ").title())
        ax.set_xlabel("Input size (n)")
        ax.set_ylabel("Time (seconds)")
        ax.legend()
        ax.grid(True, alpha=0.3)

    fig.suptitle("Deterministic vs Randomized Quicksort: Running Time by Input Distribution")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    print(f"Plot saved to {path}")


if __name__ == "__main__":
    results = run_benchmarks()
    write_csv(results, "../results/timings.csv")
    plot_results(results, "../results/timings.png")
