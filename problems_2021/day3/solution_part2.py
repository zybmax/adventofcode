"""https://adventofcode.com/2021/day/4#part2"""
import os
import os.path
from typing import List, Tuple
import itertools
import math

import numpy as np


def main():
    binary_strings = _read_data(data_file_path=os.path.join(os.path.dirname(__file__), "data.txt"))

    print(_compute_rating(binary_strings, most_common=True) * _compute_rating(binary_strings, most_common=False))


def _read_data(data_file_path: str) -> List[str]:
    with open(data_file_path, "r") as file:
        lines = file.readlines()

    return [line.rstrip() for line in lines]


def _compute_rating(binary_strings: List[str], most_common: bool = True) -> int:
    """Returns rating number based on most/least common criterion."""
    keep = [True] * len(binary_strings)
    num_left = len(binary_strings)

    for position in range(len(binary_strings[0])):
        chosen_num = _find_most_common(binary_nums=[int(x[position]) for i, x in enumerate(binary_strings) if keep[i]])
        if not most_common:
            chosen_num = int(not chosen_num)

        print(f"Position {position}, chosen digit {chosen_num}.")

        for i, string in enumerate(binary_strings):
            if not keep[i]:
                continue

            if int(string[position]) != chosen_num:
                print(f"String {i} eliminated.")

                keep[i] = False
                num_left -= 1

        if num_left == 1:
            return int(binary_strings[keep.index(True)], 2)


def _find_most_common(binary_nums: List[int]) -> int:
    """Find most common binary number.

    Inputs must be 0 or 1. If equal number, return 1.
    """
    num_zeros = 0
    num_ones = 0

    # If count is more than half length, can terminate.
    winning_count = len(binary_nums) // 2 + 1
    for i, num in enumerate(binary_nums):
        if num == 0:
            num_zeros += 1
            if num_zeros >= winning_count:
                return 0
            continue

        num_ones += 1
        if num_ones >= winning_count:
            return 1

    # Equal count, return 1.
    return 1


if __name__ == "__main__":
    main()
