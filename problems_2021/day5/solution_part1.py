"""https://adventofcode.com/2021/day/5#part2"""
import os
import os.path
from typing import List, Tuple
import re

from collections import Counter


def main():
    start_end_points = _filter_vertical_and_horizontal(
        _read_data(data_file_path=os.path.join(os.path.dirname(__file__), "data.txt"))
    )

    counts_by_coordinate = Counter()
    for start_point, end_point in start_end_points:
        is_vertical = start_point[1] == end_point[1]

        fixed_axis = 1 if is_vertical else 0
        moving_axis = 0 if is_vertical else 1

        start_index = min(start_point[moving_axis], end_point[moving_axis])
        # End point is exclusive.
        end_index = max(start_point[moving_axis], end_point[moving_axis]) + 1

        if is_vertical:
            for index in range(start_index, end_index):
                counts_by_coordinate[(index, start_point[fixed_axis])] += 1
        else:
            for index in range(start_index, end_index):
                counts_by_coordinate[(start_point[fixed_axis], index)] += 1

    print(len([coordinate for coordinate in counts_by_coordinate if counts_by_coordinate[coordinate] > 1]))


def _read_data(data_file_path: str) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
    with open(data_file_path, "r") as file:
        lines = file.readlines()

    ret = []
    for line in lines:
        nums = [int(x) for x in re.split(",| -> ", line.lstrip().rstrip())]
        ret.append(((nums[1], nums[0]), (nums[3], nums[2])))

    return ret


def _filter_vertical_and_horizontal(
    start_end_points: List[Tuple[Tuple[int, int], Tuple[int, int]]]
) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
    return [x for x in start_end_points if x[0][0] == x[1][0] or x[0][1] == x[1][1]]


if __name__ == "__main__":
    main()
