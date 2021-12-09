"""https://adventofcode.com/2021/day/9"""
import os.path

import numpy as np
from skimage.feature import peak_local_max


def main():
    height_map = _read_data(
        data_file_path=os.path.join(os.path.dirname(__file__), "data.txt")
    )

    peak_coordinates = peak_local_max(
        -height_map.astype(int) + 10,
        footprint=np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], dtype=bool),
        exclude_border=False,
    )

    result = 0
    for peak_coordinate in peak_coordinates:
        result += height_map[peak_coordinate[0], peak_coordinate[1]] + 1

    print(result)


def _read_data(data_file_path: str) -> np.ndarray:
    with open(data_file_path, "r") as file:
        lines = file.readlines()

    return np.array([[int(x) for x in line.lstrip().rstrip()] for line in lines])


if __name__ == "__main__":
    main()
