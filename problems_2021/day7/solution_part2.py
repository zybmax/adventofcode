"""https://adventofcode.com/2021/day/6"""
import os
import os.path
from typing import List

import numpy as np


def main():
    positions = np.array(
        _read_data(data_file_path=os.path.join(os.path.dirname(__file__), "data.txt"))
    )

    # Mean minimizes the sum of squared distances from all points.
    mean_position = np.mean(positions)
    # Try both the floor and ceil, and pick whichever is smaller in the squared distance.
    cost_floor = _cost(
        alignment_position=np.floor(mean_position), starting_positions=positions
    )
    cost_ceil = _cost(
        alignment_position=np.ceil(mean_position), starting_positions=positions
    )
    print(min(cost_floor, cost_ceil))


def _read_data(data_file_path: str) -> List[int]:
    with open(data_file_path, "r") as file:
        line = file.readline()

    return [int(x) for x in line.lstrip().rstrip().split(",")]


def _cost(alignment_position: int, starting_positions: np.ndarray) -> int:
    distances = np.abs(starting_positions - alignment_position)
    return int(np.sum(0.5 * distances * (distances + 1)))


if __name__ == "__main__":
    main()
