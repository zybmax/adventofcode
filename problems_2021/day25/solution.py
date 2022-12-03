"""https://adventofcode.com/2021/day/25."""
from typing import Optional, Tuple
import functools
import itertools
import numpy as np
import os


def main():
    sea_cucumber_map = _read_data(data_file_path=os.path.join(os.path.dirname(__file__), "data.txt"))

    step = 0
    while True:
        step += 1
        new_sea_cucumber_map = _move(sea_cucumber_map)
        if np.all(new_sea_cucumber_map == sea_cucumber_map):
            print(step)
            break

        sea_cucumber_map = new_sea_cucumber_map


def _move(sea_cucumber_map: np.ndarray) -> np.ndarray:
    """Returns the new sea cucumber map after one step without modifying the original input."""
    # The east movement map, where the ones that should move east are True.
    movement_mask = np.logical_and(np.roll(sea_cucumber_map, shift=(0, -1), axis=(0, 1)) == 0, sea_cucumber_map == 2)
    updated_sea_cucumber_map = np.roll(
        sea_cucumber_map * movement_mask, shift=(0, 1), axis=(0, 1)
    ) + sea_cucumber_map * np.logical_not(movement_mask)
    # Then treat the south movement.
    movement_mask = np.logical_and(
        np.roll(updated_sea_cucumber_map, shift=(-1, 0), axis=(0, 1)) == 0, updated_sea_cucumber_map == 1
    )
    return np.roll(
        updated_sea_cucumber_map * movement_mask, shift=(1, 0), axis=(0, 1)
    ) + updated_sea_cucumber_map * np.logical_not(movement_mask)


def _read_data(data_file_path: str) -> np.ndarray:
    """Returns the sea cucumber map where east are represented by 2, south 1, and empty space 0."""
    with open(data_file_path, "r") as file:
        lines = file.readlines()

    lines = list(map(lambda x: x.strip(), lines))
    ret = np.zeros((len(lines), len(lines[0])), dtype=int)
    for i, j in itertools.product(range(len(lines)), range(len(lines[0]))):
        ret[i, j] = {">": 2, "v": 1, ".": 0}[lines[i][j]]

    return ret


if __name__ == "__main__":
    main()
