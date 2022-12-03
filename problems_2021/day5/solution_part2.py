"""https://adventofcode.com/2021/day/5#part2"""
import os
import os.path
import re
from collections import Counter
from typing import List, Tuple


def main():
    start_end_points = _read_data(data_file_path=os.path.join(os.path.dirname(__file__), "data.txt"))

    counts_by_coordinate = Counter()
    for start_point, end_point in start_end_points:
        if start_point[1] == end_point[1]:
            mode = "vertical"
        elif start_point[0] == end_point[0]:
            mode = "horizontal"
        else:
            mode = "diagonal"

        if mode in {"vertical", "horizontal"}:
            is_vertical = mode == "vertical"
            fixed_axis = 1 if is_vertical else 0
            moving_axis = 0 if is_vertical else 1

            if is_vertical:
                for index in _range_from_start_end(start_point[moving_axis], end_point[moving_axis]):
                    counts_by_coordinate[(index, start_point[fixed_axis])] += 1
            else:
                for index in _range_from_start_end(start_point[moving_axis], end_point[moving_axis]):
                    counts_by_coordinate[(start_point[fixed_axis], index)] += 1

            continue

        # The mode is diagonal.
        for i, j in zip(
            _range_from_start_end(start_point[0], end_point[0]), _range_from_start_end(start_point[1], end_point[1]),
        ):
            counts_by_coordinate[(i, j)] += 1

    print(len([coordinate for coordinate in counts_by_coordinate if counts_by_coordinate[coordinate] > 1]))


def _range_from_start_end(start, end):
    # Both start and end are inclusive.
    if end >= start:
        return range(start, end + 1)

    return range(start, end - 1, -1)


def _read_data(data_file_path: str) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
    with open(data_file_path, "r") as file:
        lines = file.readlines()

    ret = []
    for line in lines:
        nums = [int(x) for x in re.split(",| -> ", line.lstrip().rstrip())]
        ret.append(((nums[1], nums[0]), (nums[3], nums[2])))

    return ret


if __name__ == "__main__":
    main()
