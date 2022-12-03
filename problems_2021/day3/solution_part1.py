"""https://adventofcode.com/2021/day/4#part2"""
import math
import os
import os.path
from typing import List


def main():
    binary_strings = _read_data(data_file_path=os.path.join(os.path.dirname(__file__), "data.txt"))
    string_length = len(binary_strings[0])

    gamma = ""
    epsilon = ""
    for i in range(string_length):
        most_common = _find_most_common([int(x[i]) for x in binary_strings])
        gamma = gamma + str(most_common)
        epsilon = epsilon + str(int(not most_common))

    print(int(gamma, 2) * int(epsilon, 2))


def _read_data(data_file_path: str) -> List[str]:
    with open(data_file_path, "r") as file:
        lines = file.readlines()

    return [line.rstrip() for line in lines]


def _find_most_common(binary_nums: List[int]) -> int:
    """Find most common binary number.

    Inputs must be 0 or 1.
    """
    num_zeros = 0
    num_ones = 0

    # If count reaches half length, can terminate.
    half_length = math.ceil(len(binary_nums) / 2)
    for i, num in enumerate(binary_nums):
        if num == 0:
            num_zeros += 1
            if num_zeros >= half_length:
                return 0
            continue

        num_ones += 1
        if num_ones >= half_length:
            return 1


if __name__ == "__main__":
    main()
