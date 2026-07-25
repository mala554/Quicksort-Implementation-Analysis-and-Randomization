"""
quicksort.py

Deterministic (last-element pivot) and randomized implementations of
the Quicksort algorithm, using the Lomuto partition scheme.

Author: Kelvin
Assignment 5: Quicksort Algorithm: Implementation, Analysis, and Randomization
"""

import random


def partition(arr, low, high):
    """
    Lomuto partition scheme.

    Uses the last element of arr[low..high] as the pivot. Elements
    smaller than or equal to the pivot are moved to its left, larger
    elements stay to its right. Returns the final index of the pivot.

    Args:
        arr: list to partition in place.
        low: starting index of the subarray.
        high: ending index of the subarray (pivot index).

    Returns:
        int: the index where the pivot ends up after partitioning.
    """
    pivot = arr[high]
    i = low - 1  # index of the last element known to be <= pivot

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def quicksort(arr, low=0, high=None):
    """
    Deterministic Quicksort. Always chooses the last element of the
    current subarray as the pivot.

    Sorts arr in place. On the first call, low/high default to the
    full array bounds.

    Args:
        arr: list to sort in place.
        low: starting index (default 0).
        high: ending index (default len(arr) - 1).
    """
    if high is None:
        high = len(arr) - 1

    if low < high:
        pivot_index = partition(arr, low, high)
        quicksort(arr, low, pivot_index - 1)
        quicksort(arr, pivot_index + 1, high)

    return arr


def randomized_partition(arr, low, high):
    """
    Partition helper for randomized Quicksort.

    Picks a uniformly random index in arr[low..high], swaps it into
    the last position, then delegates to the standard Lomuto
    partition so the rest of the recursion is identical to the
    deterministic version.

    Args:
        arr: list to partition in place.
        low: starting index of the subarray.
        high: ending index of the subarray.

    Returns:
        int: the index where the (randomly chosen) pivot ends up.
    """
    random_index = random.randint(low, high)
    arr[random_index], arr[high] = arr[high], arr[random_index]
    return partition(arr, low, high)


def randomized_quicksort(arr, low=0, high=None):
    """
    Randomized Quicksort. Chooses a uniformly random pivot from the
    current subarray at every recursive call.

    Sorts arr in place. On the first call, low/high default to the
    full array bounds.

    Args:
        arr: list to sort in place.
        low: starting index (default 0).
        high: ending index (default len(arr) - 1).
    """
    if high is None:
        high = len(arr) - 1

    if low < high:
        pivot_index = randomized_partition(arr, low, high)
        randomized_quicksort(arr, low, pivot_index - 1)
        randomized_quicksort(arr, pivot_index + 1, high)

    return arr


if __name__ == "__main__":
    sample = [9, 4, 7, 1, 8, 3, 6, 2, 5, 0]

    print("Original array:           ", sample)
    print("Deterministic quicksort:  ", quicksort(sample.copy()))
    print("Randomized quicksort:     ", randomized_quicksort(sample.copy()))

    # Edge cases
    print("Empty array:              ", quicksort([]))
    print("Single element:           ", quicksort([42]))
    print("Already sorted:           ", quicksort([1, 2, 3, 4, 5]))
    print("Reverse sorted:           ", quicksort([5, 4, 3, 2, 1]))
    print("Duplicates:               ", quicksort([3, 1, 3, 3, 2, 1]))
