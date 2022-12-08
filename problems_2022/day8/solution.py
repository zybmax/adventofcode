"""https://adventofcode.com/2022/day/8."""
import os
import itertools
from typing import Tuple, List

import numpy as np

from adventofcode.util import read_lines_stripping_both_ends


def main():
    tree_height_matrix = _read_data(data_file_path=os.path.join(os.path.dirname(__file__), "data.txt"))
    visible_mask, visibility_range_maps = _visible_mask_and_visilility_range_maps(tree_height_matrix=tree_height_matrix)
    print(f"Part 1: The number of visible trees is {np.sum(visible_mask)}.")

    visibility_scores = np.prod(np.stack(visibility_range_maps, axis=0), axis=0)
    print(f"Part 2: The maximum visibility score is {np.max(visibility_scores)}.")


def _read_data(data_file_path: str) -> np.ndarray:
    array = []
    for line in read_lines_stripping_both_ends(file_path=data_file_path):
        array.append([int(x) for x in line])
    return np.array(array, dtype=int)


def _visible_mask_and_visilility_range_maps(tree_height_matrix: np.ndarray) -> Tuple[np.ndarray, List[np.ndarray]]:
    visibility_mask = np.zeros_like(tree_height_matrix, dtype=bool)

    visibility_range_maps = []
    for search_axis, direction in itertools.product([0, 1], [1, -1]):
        # The visibility range map is a 2D array representing the number of trees a position can see, in a given
        # direction.
        visibility_range_map = np.zeros_like(tree_height_matrix, dtype=int)

        # `search_axis` is the axis of the inner loop, to search for trees that are visible. `search_axis == 0` means
        # that the inner loop will search a column at a time.
        other_axis = 1 - search_axis
        for index_other_axis in range(tree_height_matrix.shape[other_axis]):
            # All tree heights are positive, so initialize maximum to -1 to be lower than all possible heights.
            maximum = -1

            # `last_positions` records the last position (index) of each tree height.
            last_positions = np.zeros(shape=(tree_height_matrix.shape[search_axis],), dtype=int)
            for index_current_axis in range(tree_height_matrix.shape[search_axis]):
                if direction == -1:
                    current_index = tree_height_matrix.shape[search_axis] - 1 - index_current_axis
                else:
                    current_index = index_current_axis

                index_2d = (current_index, index_other_axis) if search_axis == 0 else (index_other_axis, current_index)

                tree_height = tree_height_matrix[index_2d[0], index_2d[1]]
                if tree_height > maximum:
                    maximum = tree_height
                    visibility_mask[index_2d[0], index_2d[1]] = True

                visibility_range_map[index_2d[0], index_2d[1]] = index_current_axis - np.max(
                    last_positions[tree_height:]
                )
                last_positions[tree_height] = index_current_axis

        visibility_range_maps.append(visibility_range_map)

    return visibility_mask, visibility_range_maps


if __name__ == "__main__":
    main()
