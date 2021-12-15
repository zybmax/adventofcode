"""https://adventofcode.com/2021/day/15.

Use depth-first search to explore all possible paths. After a path if found, we can terminate other paths if the total
risk is equal to or higher than the risk of the existing path.  There is no use to visit points that have already been
visited (which will lead to higher risks), so we should keep the coordinates that have already been visited in a list
or set.
"""
import os.path
from typing import List
from typing import Tuple, Set
import itertools

import numpy as np


_Point = Tuple[int, int]


def main():
    risk_level_map = _read_data(data_file_path=os.path.join(os.path.dirname(__file__), "data.txt"))

    print(_PathFinder(risk_level_map=risk_level_map).lowest_total_risk)


def _read_data(data_file_path: str) -> np.ndarray:
    """Returns the risk level map."""
    with open(data_file_path, "r") as file:
        lines = file.readlines()

    return np.array([[int(x) for x in line.lstrip().rstrip()] for line in lines], dtype=np.uint8)


class _PathFinder:
    def __init__(self, risk_level_map: np.ndarray) -> None:
        self._risk_level_map: np.ndarray = risk_level_map
        self._best_total_risk = float("inf")
        self._find_lowest_total_risk(current_position=(0, 0), current_total_risk=0, forbidden_points={(0, 0)})

    @property
    def lowest_total_risk(self) -> int:
        return self._best_total_risk

    def _find_lowest_total_risk(
        self, current_position: _Point, current_total_risk: int, forbidden_points: Set[_Point],
    ) -> None:
        """Updates the `_best_total_risk` attribute.

        `current_total_risk` includes the risk of the current position.
        """
        if current_position == (self._risk_level_map.shape[0] - 1, self._risk_level_map.shape[1] - 1,):
            print(f"Found new risk: {current_total_risk}")
            self._best_total_risk = current_total_risk

        for neighbor in self._find_neighbors(current_position):
            if neighbor in forbidden_points:
                continue

            new_total_risk = current_total_risk + self._risk_level_map[neighbor[0], neighbor[1]]

            if new_total_risk > self._best_total_risk:
                continue

            self._find_lowest_total_risk(
                current_position=neighbor,
                current_total_risk=new_total_risk,
                forbidden_points=forbidden_points | {neighbor},
            )

    def _find_neighbors(self, position: _Point) -> List[_Point]:
        return [
            (position[0] + i_offset, position[1] + j_offset)
            for i_offset, j_offset in itertools.product(range(-1, 2), range(-1, 2))
            if 0 <= position[0] + i_offset < self._risk_level_map.shape[0]
            and 0 <= position[1] + j_offset < self._risk_level_map.shape[1]
            and (i_offset, j_offset) != (0, 0)
        ]


if __name__ == "__main__":
    main()
