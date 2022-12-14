"""https://adventofcode.com/2022/day/14."""
import os
from typing import Tuple

import numpy as np

from adventofcode.util import read_lines_stripping_both_ends


def main():
    source_position = np.array([0, 500])
    rock_map, top_left = _read_data(data_file_path=os.path.join(os.path.dirname(__file__), "data.txt"))

    resulting_rock_map = _simulate_until_stable_or_block_source(
        rock_map=rock_map, source_position=source_position - top_left
    )
    num_sands = np.sum(resulting_rock_map) - np.sum(rock_map)
    print(f"Part 1: The number of sands is {num_sands}.")

    rock_map[-1, :] = True
    resulting_rock_map = _simulate_until_stable_or_block_source(
        rock_map=rock_map, source_position=source_position - top_left
    )
    num_sands = np.sum(resulting_rock_map) - np.sum(rock_map)
    print(f"Part 2: The number of sands is {num_sands}.")


def _read_data(data_file_path: str) -> Tuple[np.ndarray, np.ndarray]:
    """Returns 2D boolean array where True represents rock and coordinate of the top-left element of the array."""
    # `coordinates` is a list of list of (y, x) points.
    coordinates = []

    min_x = float("inf")
    max_y = max_x = -float("inf")

    for line_idx, line in enumerate(read_lines_stripping_both_ends(file_path=data_file_path)):
        current_coordinates = []
        for xy_string in line.split(" -> "):
            x, y = tuple(int(value) for value in xy_string.split(","))
            current_coordinates.append(np.array([y, x]))

            max_y = max(max_y, y)
            min_x = min(min_x, x)
            max_x = max(max_x, x)

        coordinates.append(current_coordinates)

    # The source point is at y = 0.
    # To be able to complete part 2, we let the top row be y = 0; leave two extra rows in the bottom (for the bottom
    # floor for part 2); pad the left and right sides with the total height of the simulation space.
    height = max_y + 2 + 1
    x_padding = height
    top_left = np.array([0, min_x - x_padding], dtype=int)
    ret = np.zeros(shape=(height, max_x - min_x + 1 + 2 * x_padding), dtype=bool)

    for current_coordinates in coordinates:
        for point_idx in range(1, len(current_coordinates)):
            # Minus the top-left coordinate to compute the coordinate in the returned rock map.
            this_point, previous_point = (
                current_coordinates[point_idx] - top_left,
                current_coordinates[point_idx - 1] - top_left,
            )

            static_axis = np.where((previous_point - this_point) == 0)[0][0]
            changing_axis = 1 - static_axis

            for coordinate in range(
                min(previous_point[changing_axis], this_point[changing_axis]),
                max(previous_point[changing_axis], this_point[changing_axis]) + 1,
            ):
                if static_axis == 0:
                    ret[previous_point[0], coordinate] = True
                else:
                    ret[coordinate, previous_point[1]] = True

    return ret, top_left


def _simulate_until_stable_or_block_source(rock_map: np.ndarray, source_position: np.ndarray) -> np.ndarray:
    """Returns the rock map after the all sands are stable or a sand blocks the source position."""
    rock_map = rock_map.copy()
    source_x = source_position[1]

    while True:
        # A sand falls from the source position downwards until it touches a rock.
        sand_x = source_x
        sand_y = 0

        if rock_map[sand_y, sand_x]:
            # The source position is blocked (only applies to part 2).
            return rock_map

        while True:
            try:
                # Stop when the sand hits a rock or sand.
                sand_y = np.where(rock_map[sand_y:, sand_x] == True)[0][0] + sand_y - 1
            except IndexError:
                # Cannot find a stopping position.  This means that the sand has moved out of frame, and the algorithm
                # has converged.
                return rock_map

            # Determine the next position. Already know that it cannot move down directly.
            if not rock_map[sand_y + 1, sand_x - 1]:
                # Can move down-left.
                sand_y, sand_x = sand_y + 1, sand_x - 1
                continue

            if not rock_map[sand_y + 1, sand_x + 1]:
                # Can move down-right.
                sand_y, sand_x = sand_y + 1, sand_x + 1
                continue

            # Reached a resting position.
            rock_map[sand_y, sand_x] = True
            break


if __name__ == "__main__":
    main()
