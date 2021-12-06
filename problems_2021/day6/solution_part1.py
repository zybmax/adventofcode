"""https://adventofcode.com/2021/day/5#part2"""
import os
import os.path
from typing import List, Tuple
import re

from collections import Counter


def main():
    days_left = _read_data(
        data_file_path=os.path.join(os.path.dirname(__file__), "data.txt")
    )

    num_days = 256

    for day in range(num_days):
        for index_fish in range(len(days_left)):
            if days_left[index_fish] == 0:
                days_left[index_fish] = 6
                days_left.append(8)
            else:
                days_left[index_fish] -= 1

    print(len(days_left))


def _read_data(data_file_path: str) -> List[int]:
    with open(data_file_path, "r") as file:
        line = file.readline()

    return [int(x) for x in line.lstrip().rstrip().split(",")]


if __name__ == "__main__":
    main()
