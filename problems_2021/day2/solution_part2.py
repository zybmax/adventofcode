"""https://adventofcode.com/2021/day/2"""
import os
import os.path
from typing import List, Tuple


def main():
    commands_and_distances = _read_data(data_file_path=os.path.join(os.path.dirname(__file__), "data.txt"))

    y, x, aim = 0, 0, 0

    for command, distance in commands_and_distances:
        if command == "down":
            aim += distance
        elif command == "up":
            aim -= distance
        else:
            x += distance
            y += aim * distance

        print(y, x, aim)

    print(y * x)


def _read_data(data_file_path: str) -> List[Tuple[str, int]]:
    """Returns the (command, distance) tuples of all steps."""
    with open(data_file_path, "r") as file:
        lines = file.readlines()

    ret = []
    for line in lines:
        command, distance = line.lstrip().rstrip().split()
        distance = int(distance)
        ret.append((command, distance))

    return ret


if __name__ == "__main__":
    main()
