"""https://adventofcode.com/2022/day/3."""
import os
from typing import List, Tuple

from adventofcode.util import read_lines_stripping_both_ends


def main():
    inputs = _read_data(data_file_path=os.path.join(os.path.dirname(__file__), "data.txt"))

    sum_priorities = 0
    for left, right in inputs:
        common_letter = set(left).intersection(set(right))
        if len(common_letter) != 1:
            raise RuntimeError(f"Number of common letters is not 1 between {left} and {right}!")
        common_letter = next(iter(common_letter))
        sum_priorities += letter_to_priority(letter=common_letter)
    print(f"Part 1: The sum of priorities is {sum_priorities}.")


def _read_data(data_file_path: str) -> List[Tuple[str, str]]:
    lines = read_lines_stripping_both_ends(file_path=data_file_path)

    ret = []
    for line in lines:
        length = len(line)
        ret.append((line[: length // 2], line[length // 2 :]))

    return ret


def letter_to_priority(letter: str) -> int:
    num = ord(letter)
    if num < 97:
        # The number if a capital letter.  "A" has ASCII value of 65.
        return num - 64 + 26

    # The number if a lowercase letter.  "a" has ASCII value of 97.
    return ord(letter) - 96


if __name__ == "__main__":
    main()
