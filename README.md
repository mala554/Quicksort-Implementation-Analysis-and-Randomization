# Quicksort: Implementation, Analysis, and Randomization

Assignment 5 deliverable. Contains deterministic and randomized Python implementations of Quicksort, an empirical benchmarking script, and a written report.


## Requirements

- Python 3.8+
- matplotlib (only needed to regenerate the plot: `pip install matplotlib`)

## How to Run

Run the implementation directly (includes a small self-test on sample arrays):

```bash
cd src
python3 quicksort.py
```

Run the empirical benchmark (regenerates `results/timings.csv` and `results/timings.png`):

```bash
cd src
python3 empirical_analysis.py
```

To use the sorting functions in your own code:

```python
from quicksort import quicksort, randomized_quicksort

data = [5, 3, 8, 1, 9, 2]
quicksort(data)              # sorts in place, last element as pivot
randomized_quicksort(data)   # sorts in place, random pivot each call
```

## Summary of Findings

Both versions of Quicksort use an in-place Lomuto partition. The deterministic version always pivots on the last element of the current subarray; the randomized version swaps a uniformly random element into that position first.

Benchmarking both versions on random, sorted, and reverse-sorted input across sizes from 100 to 6,000 elements showed:

- **Random input:** the two versions perform similarly, both close to their O(n log n) average case. The deterministic version is marginally faster since it skips the cost of generating random numbers.
- **Sorted and reverse-sorted input:** the deterministic version degrades to O(n^2), taking just over one second to sort 6,000 already-sorted elements, since always picking the last element as pivot produces a maximally unbalanced partition at every step. The randomized version is unaffected by input order and stays under seven milliseconds across the same range, consistent with its O(n log n) expected running time.

This confirms the theoretical result: randomizing pivot selection does not lower the worst-case bound in an absolute sense, but it decouples that worst case from any specific, predictable input pattern, making the randomized version far more reliable in practice.

