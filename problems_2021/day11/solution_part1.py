"""https://adventofcode.com/2021/day/11"""
import itertools
import os.path
from typing import List
from typing import Tuple

import numpy as np


def main():
    energy_level_map = _read_data(
        data_file_path=os.path.join(os.path.dirname(__file__), "data.txt")
    )

    print(sum(_simulate_one_step(energy_level_map) for _ in range(100)))


def _read_data(data_file_path: str) -> np.ndarray:
    with open(data_file_path, "r") as file:
        lines = file.readlines()

    return np.array(
        [[int(x) for x in line.lstrip().rstrip()] for line in lines], dtype=np.uint8
    )


def _simulate_one_step(energy_level_map: np.ndarray) -> int:
    """Changes the energy level map in-place; returns the flashes in the current step."""
    energy_level_map += 1
    num_flashes = 0

    all_saturated_indices = []
    while True:
        saturated_indices = _find_saturated_indices(energy_level_map)
        if len(saturated_indices) == 0:
            break

        num_flashes += len(saturated_indices)
        all_saturated_indices.extend(saturated_indices)

        for i, j in saturated_indices:
            for neighbor in _find_neighbors((i, j), energy_level_map.shape):
                if neighbor not in all_saturated_indices:
                    energy_level_map[neighbor[0], neighbor[1]] += 1

            for i, j in saturated_indices:
                energy_level_map[i, j] = 0

    for i, j in all_saturated_indices:
        energy_level_map[i, j] = 0

    return num_flashes


def _find_saturated_indices(energy_level_map: np.ndarray) -> List[Tuple[int, int]]:
    return [(i.item(), j.item()) for i, j in zip(*np.where(energy_level_map > 9))]


def _find_neighbors(
    point: Tuple[int, int], shape: Tuple[int, int]
) -> List[Tuple[int, int]]:
    ret = []
    for i_offset, j_offset in itertools.product(range(-1, 2), range(-1, 2)):
        if (
            0 <= point[0] + i_offset < shape[0]
            and 0 <= point[1] + j_offset < shape[1]
            and (i_offset, j_offset) != (0, 0)
        ):
            ret.append((point[0] + i_offset, point[1] + j_offset))

    return ret


if __name__ == "__main__":
    main()
