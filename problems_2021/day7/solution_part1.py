"""https://adventofcode.com/2021/day/6"""
import os
import os.path
from typing import List

import numpy as np


def main():
    positions = np.array(
        _read_data(data_file_path=os.path.join(os.path.dirname(__file__), "data.txt"))
    )

    # Median minimizes the l1 distance from all points.
    # Ref: https://math.stackexchange.com/a/113336
    sum_distance_from_median = np.sum(np.abs(positions - np.median(positions)))
    print(int(sum_distance_from_median))


def _read_data(data_file_path: str) -> List[int]:
    with open(data_file_path, "r") as file:
        line = file.readline()

    return [int(x) for x in line.lstrip().rstrip().split(",")]


if __name__ == "__main__":
    main()
