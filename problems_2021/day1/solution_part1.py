"""https://adventofcode.com/2021/day/1"""
import os
import os.path
from typing import List


def main():
    depths = _read_data(data_file_path=os.path.join(os.path.dirname(__file__), "data.txt"))

    count = 0
    for i in range(len(depths) - 1):
        if depths[i + 1] > depths[i]:
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
