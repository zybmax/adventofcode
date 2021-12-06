"""https://adventofcode.com/2021/day/1"""
import os
import os.path
from typing import List
from scipy.signal import convolve

from collections import Counter


def main():
    depths = _read_data(
        data_file_path=os.path.join(os.path.dirname(__file__), "data.txt")
    )

    filtered_depths = convolve(depths, [1, 1, 1], mode="valid", method="direct")

    count = 0
    for i in range(len(filtered_depths) - 1):
        if filtered_depths[i + 1] > filtered_depths[i]:
            count += 1

    print(count)


def _read_data(data_file_path: str) -> List[int]:
    with open(data_file_path, "r") as file:
        lines = file.readlines()

    ret = []
    for line in lines:
        ret.append(int(line.lstrip().rstrip()))

    return ret


if __name__ == "__main__":
    main()
