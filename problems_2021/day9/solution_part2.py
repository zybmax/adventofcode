"""https://adventofcode.com/2021/day/9"""
import os.path
from typing import List
from typing import Tuple

import numpy as np
from skimage.feature import peak_local_max


def main():
    height_map = _read_data(data_file_path=os.path.join(os.path.dirname(__file__), "data.txt"))

    # Need to take the negative because `peak_local_max` finds peaks not valleys.  Need to also add 10 to make all
    # heights positive, because under the hood `peak_local_max` uses a max filter with zero padding on the boundaries.
    # If the heights are negatives, the low points on the boundaries will be wrongly missed.
    peak_coordinates = peak_local_max(
        -height_map.astype(int) + 10,
        footprint=np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], dtype=bool),
        exclude_border=False,
    )

    basin_mask = np.zeros(shape=height_map.shape, dtype=bool)
    point_collections = [[] for _ in range(len(peak_coordinates))]
    for peak_coordinate, point_collection in zip(peak_coordinates, point_collections):
        _flood_fill(
            point=tuple(peak_coordinate), height_map=height_map, basin_mask=basin_mask, points_in_basin=point_collection
        )

    # Remove duplicates.
    unique_basin_point_collections = []
    all_basin_points = []
    for point_collection in point_collections:
        # Skip duplicate basins.
        if point_collection[0] in all_basin_points:
            continue

        unique_basin_point_collections.append(point_collection)
        all_basin_points.extend(point_collection)

    # Find the size of the three largest basins.
    largest_sizes = sorted(len(x) for x in unique_basin_point_collections)[-3:]
    print(np.prod(largest_sizes).item())


def _read_data(data_file_path: str) -> np.ndarray:
    with open(data_file_path, "r") as file:
        lines = file.readlines()

    return np.array([[int(x) for x in line.lstrip().rstrip()] for line in lines])


def _flood_fill(
    point: Tuple[int, int], height_map: np.ndarray, basin_mask: np.ndarray, points_in_basin: List[Tuple[int, int]]
) -> None:
    """Recursively updates `basin_mask` and puts valid basin points to `points_in_basin`."""
    # Out of bounds.
    if not (0 <= point[0] < height_map.shape[0] and 0 <= point[1] < height_map.shape[1]):
        return

    # Hit a wall.
    if height_map[point[0], point[1]] == 9:
        return

    # Already visited.
    if basin_mask[point[0], point[1]]:
        return

    basin_mask[point[0], point[1]] = True
    points_in_basin.append(point)

    _flood_fill((point[0] - 1, point[1]), height_map=height_map, basin_mask=basin_mask, points_in_basin=points_in_basin)
    _flood_fill((point[0] + 1, point[1]), height_map=height_map, basin_mask=basin_mask, points_in_basin=points_in_basin)
    _flood_fill((point[0], point[1] - 1), height_map=height_map, basin_mask=basin_mask, points_in_basin=points_in_basin)
    _flood_fill((point[0], point[1] + 1), height_map=height_map, basin_mask=basin_mask, points_in_basin=points_in_basin)


if __name__ == "__main__":
    main()
