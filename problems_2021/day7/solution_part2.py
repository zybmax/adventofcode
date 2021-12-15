"""https://adventofcode.com/2021/day/7"""
import os
import os.path
from typing import List

import numpy as np


def main():
    positions = np.array(_read_data(data_file_path=os.path.join(os.path.dirname(__file__), "data.txt")))

    # Mean minimizes the sum of squared distances from all points.
    mean_position = np.mean(positions)
    # The gradient of the total cost is:
    # 1/n df/fx = x - mu + 1/2n sum_i(sng(x - x_i)), where the last term is bounded by (-0.5, 0.5). Therefore, the
    # fractional optimal position must reside in (mean - 0.5, mean + 0.5). Therefore, only need to check the floor and
    # ceil of both (mean - 0.5) and (mean + 0.5).
    positions_to_check = {
        np.floor(mean_position - 0.5),
        np.ceil(mean_position - 0.5),
        np.floor(mean_position + 0.5),
        np.ceil(mean_position + 0.5),
    }

    print(min([_cost(alignment_position=x, starting_positions=positions) for x in positions_to_check]))


def _read_data(data_file_path: str) -> List[int]:
    with open(data_file_path, "r") as file:
        line = file.readline()

    return [int(x) for x in line.lstrip().rstrip().split(",")]


def _cost(alignment_position: int, starting_positions: np.ndarray) -> int:
    distances = np.abs(starting_positions - alignment_position)
    return int(np.sum(0.5 * distances * (distances + 1)))


if __name__ == "__main__":
    main()
