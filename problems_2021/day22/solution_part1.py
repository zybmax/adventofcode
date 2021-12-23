"""https://adventofcode.com/2021/day/22."""
import os.path
from typing import List
from typing import Tuple

import numpy as np


# Interval with both sides inclusive.
_Interval = Tuple[int, int]
# A step is defined as (to_turn_on, (y_interval, x_interval, z_interval)).
_Step = Tuple[bool, Tuple[_Interval, _Interval, _Interval]]


def main():
    steps = _read_data(data_file_path=os.path.join(os.path.dirname(__file__), "data.txt"))

    # Part 1.
    # Array has dims of y, x, z.
    array = np.zeros((101, 101, 101), dtype=bool)
    start_point = (-50, -50, -50)

    for to_turn_on, interval_3d in steps:
        slice_3d = ()
        for (min_coordinate, max_coordinate), start_coordinate, length_in_dim in zip(
            interval_3d, start_point, array.shape
        ):
            slice_3d = (
                slice_3d
                + np.index_exp[
                    max(0, min_coordinate - start_coordinate) : max(
                        0, min(length_in_dim, max_coordinate - start_coordinate + 1)
                    )
                ]
            )
        array[slice_3d] = to_turn_on

    print(np.sum(array).item())


def _read_data(data_file_path: str) -> List[_Step]:
    """Returns a list of steps."""
    with open(data_file_path, "r") as file:
        lines = file.readlines()

    ret = []
    for line in lines:
        line = line.strip()
        if line.startswith("on"):
            to_turn_on = True
            line = line[len("on ") :]
        else:
            to_turn_on = False
            line = line[len("off ") :]

        # Remove "x=", "y=" or "z=" from each substring before splitting by "..".
        intervals = tuple(tuple(int(x) for x in substring[2:].split("..")) for substring in line.split(","))
        # Convert to y, x, z ordering to be consistent with numpy convention.
        intervals = (intervals[1], intervals[0], intervals[2])

        ret.append((to_turn_on, intervals))

    return ret


if __name__ == "__main__":
    main()
