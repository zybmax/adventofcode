"""https://adventofcode.com/2021/day/13."""
import os.path
from typing import List
from typing import Set
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np


_Point = Tuple[int, int]
_PointSet = Set[_Point]


def main():
    point_set, fold_instructions = _read_data(data_file_path=os.path.join(os.path.dirname(__file__), "data.txt"))

    # Part 1.
    _fold(
        point_set=point_set, axis=fold_instructions[0][0], position=fold_instructions[0][1],
    )
    print("Part 1: ", len(point_set))

    # Part 2.
    for axis, position in fold_instructions[1:]:
        _fold(point_set=point_set, axis=axis, position=position)

    image = np.zeros(shape=(max(y for y, x in point_set) + 1, max(x for y, x in point_set) + 1), dtype=bool,)
    for point in point_set:
        image[point[0], point[1]] = True
    plt.figure()
    plt.imshow(image)
    plt.title("Part 2")
    plt.show()


def _read_data(data_file_path: str) -> Tuple[_PointSet, List[Tuple[int, int]]]:
    """Returns the original point set and a list of (fold_axis, row_or_col_num) tuples.

    `fold_axis` is 0 if to be folded along a certain row, or 1 if to be folded along a certain column.
    """
    with open(data_file_path, "r") as file:
        lines = file.readlines()

    point_set = set()
    fold_instructions = []

    parse_point_set = True
    for line in lines:
        line = line.lstrip().rstrip()

        # An empty line is the separator between the point set and the folding instructions.
        if not line:
            parse_point_set = False
            continue

        if parse_point_set:
            x, y = line.split(",")
            point_set.add((int(y), int(x)))
            continue

        # Each folding instruction starts with the string "fold along ".
        axis, num = line[len("fold along ") :].split("=")
        fold_instructions.append((0 if axis == "y" else 1, int(num)))

    return point_set, fold_instructions


def _fold(point_set: _PointSet, axis: int, position: int):
    """Folds `point_set` along `axis` at `position`; in-place modifies `point_set`."""
    for point in point_set.copy():
        if point[axis] > position:
            point_set.add((2 * position - point[0], point[1]) if axis == 0 else (point[0], 2 * position - point[1]))
            point_set.remove(point)


if __name__ == "__main__":
    main()
