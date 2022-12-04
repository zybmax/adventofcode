"""https://adventofcode.com/2022/day/3."""
import os
from typing import List, Tuple

from adventofcode.util import read_lines_stripping_both_ends
from problems_2022.day3.solution_part1 import letter_to_priority


def main():
    inputs = _read_data(data_file_path=os.path.join(os.path.dirname(__file__), "data.txt"))

    sum_priorities = 0
    num_lines = len(inputs)
    for group_index in range(num_lines // 3):
        lines = inputs[group_index * 3 : group_index * 3 + 3]
        common_letter = set(lines[0]).intersection(*lines[1:])
        if len(common_letter) != 1:
            raise RuntimeError(f"Number of common letters is not 1 between {lines}!")

        common_letter = next(iter(common_letter))
        sum_priorities += letter_to_priority(letter=common_letter)

    print(f"Part 2: The sum of priorities is {sum_priorities}.")


def _read_data(data_file_path: str) -> List[str]:
    return read_lines_stripping_both_ends(file_path=data_file_path)


if __name__ == "__main__":
    main()
