"""https://adventofcode.com/2022/day/4."""
import os
from typing import List, Tuple

from adventofcode.util import read_lines_stripping_both_ends


_Range = Tuple[int, int]


def main():
    inputs = _read_data(data_file_path=os.path.join(os.path.dirname(__file__), "data.txt"))

    print(inputs)

    num_containments = sum(_one_range_contains_other(range_1=x, range_2=y) for x, y in inputs)
    print(f"Part 1: The number of cases where one range contains the other is {num_containments}.")

    num_overlaps = sum(_ranges_overlap(range_1=x, range_2=y) for x, y in inputs)
    print(f"Part 2: The number of cases where the two ranges overlap is {num_overlaps}.")


def _read_data(data_file_path: str) -> List[Tuple[_Range, _Range]]:
    lines = read_lines_stripping_both_ends(file_path=data_file_path)

    ret = []
    for line in lines:
        numbers = [int(x) for x in line.replace("-", ",").split(sep=",")]
        ret.append(((numbers[0], numbers[1]), (numbers[2], numbers[3])))

    return ret


def _one_range_contains_other(range_1: _Range, range_2: _Range) -> bool:
    if (range_1[0] <= range_2[0] and range_1[1] >= range_2[1]) or (
        range_1[0] >= range_2[0] and range_1[1] <= range_2[1]
    ):
        return True

    return False


def _ranges_overlap(range_1: _Range, range_2: _Range) -> bool:
    if range_1[1] < range_2[0] or range_2[1] < range_1[0]:
        return False

    return True


if __name__ == "__main__":
    main()
