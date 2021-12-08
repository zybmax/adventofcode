"""https://adventofcode.com/2021/day/8"""
import os.path
import re
from typing import List
from typing import Tuple


def main():
    digits_and_outputs = _read_data(
        data_file_path=os.path.join(os.path.dirname(__file__), "data.txt")
    )

    unique_lengths = {2, 4, 3, 7}
    count = 0
    for digits, outputs in digits_and_outputs:
        count += len([x for x in outputs if len(x) in unique_lengths])

    print(count)


def _read_data(data_file_path: str) -> List[Tuple[List[str], List[str]]]:
    with open(data_file_path, "r") as file:
        lines = file.readlines()

    ret = []
    for line in lines:
        strings = [
            x.lstrip().rstrip() for x in re.split(" \\| | ", line.lstrip().rstrip())
        ]
        ret.append((strings[:10], strings[10:]))

    return ret


if __name__ == "__main__":
    main()
