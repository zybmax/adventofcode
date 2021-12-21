"""https://adventofcode.com/2021/day/20."""
import itertools
import os.path
from typing import List
from typing import Tuple

import numpy as np


def main():
    algorithm, input_image = _read_data(data_file_path=os.path.join(os.path.dirname(__file__), "data.txt"))

    print("Part 1: ", np.sum(_enhance_image(input_image=input_image, pad_value=0, algorithm=algorithm, num_times=2)[0]))
    print(
        "Part 2: ", np.sum(_enhance_image(input_image=input_image, pad_value=0, algorithm=algorithm, num_times=50)[0])
    )


def _read_data(data_file_path: str) -> Tuple[np.ndarray, np.ndarray]:
    """Returns the image enhancement algorithm and the input image.

    The image enhancement algorithm is a 1D array of 0s and 1s.  The input image is a 2D array of 0s and 1s.
    """
    with open(data_file_path, "r") as file:
        lines = file.readlines()

    algorithm = np.array(_str_to_binary_int_list(lines[0].lstrip().rstrip()), dtype=int)
    input_image = np.array([_str_to_binary_int_list(line.lstrip().rstrip()) for line in lines[2:]], dtype=int)

    return algorithm, input_image


def _str_to_binary_int_list(string: str) -> List[int]:
    return [0 if x == "." else 1 for x in string]


def _enhance_image(
    input_image: np.ndarray, pad_value: int, algorithm: np.ndarray, num_times: int
) -> Tuple[np.ndarray, int]:
    """Returns the enhanced image and the infinite pad value around it."""
    enhanced = np.pad(
        input_image, pad_width=((num_times, num_times), (num_times, num_times)), constant_values=pad_value
    )

    for enhancement_round in range(num_times):
        more_enhanced = np.zeros_like(enhanced)
        for i, j in itertools.product(range(enhanced.shape[0]), range(enhanced.shape[1])):
            more_enhanced[i, j] = algorithm[
                int(
                    "".join(str(x) for x in _get_neighborhood(enhanced, point=(i, j), pad_value=pad_value).flatten()), 2
                )
            ]
        pad_value = algorithm[0] if pad_value == 0 else algorithm[int("111111111", 2)]

        enhanced = more_enhanced

    return enhanced, pad_value


def _get_neighborhood(array, point, pad_value) -> np.ndarray:
    """Returns a 3x3 neighborhood of `array` at `point`.

    If the point is at a boundary, use pad value for the invalid pixels.
    """
    if 1 <= point[0] <= array.shape[0] - 2 and 1 <= point[1] <= array.shape[1] - 2:
        return array[point[0] - 1 : point[0] + 2, point[1] - 1 : point[1] + 2]

    ret = np.zeros((3, 3), dtype=int)
    for i, j in itertools.product(range(-1, 2), range(-1, 2)):
        if 0 <= point[0] + i <= array.shape[0] - 1 and 0 <= point[1] + j <= array.shape[1] - 1:
            ret[i + 1, j + 1] = array[point[0] + i, point[1] + j]
        else:
            ret[i + 1, j + 1] = pad_value
    return ret


if __name__ == "__main__":
    main()
