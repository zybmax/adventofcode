"""https://adventofcode.com/2021/day/2"""
import os
import os.path
from typing import List, Tuple
import re

from collections import Counter


def main():
    vectors = _read_data(data_file_path=os.path.join(os.path.dirname(__file__), "data.txt"))

    final_position = (sum([x[0] for x in vectors]), sum([x[1] for x in vectors]))
    print(final_position[0] * final_position[1])


def _read_data(data_file_path: str) -> List[Tuple[int, int]]:
    """Returns the (y, x) vector of all steps."""
    with open(data_file_path, "r") as file:
        lines = file.readlines()

    ret = []
    for line in lines:
        command, distance = line.lstrip().rstrip().split()
        distance = int(distance)

        if command == "forward":
            vector = (0, distance)
        elif command == "up":
            vector = (-distance, 0)
        else:
            vector = (distance, 0)
        ret.append(vector)

    return ret


if __name__ == "__main__":
    main()
