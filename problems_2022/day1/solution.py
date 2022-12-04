"""https://adventofcode.com/2022/day/1."""
import os
from typing import List


def main():
    numbers = _read_data(data_file_path=os.path.join(os.path.dirname(__file__), "data.txt"))
    calories = [sum(x) for x in numbers]
    max_sum = max(calories)
    print(f"Part 1: The max is {max_sum}.")

    sum_of_three_max = sum(list(sorted(calories, reverse=True))[:3])
    print(f"Part 2: The sum of three maximum carried calories is {sum_of_three_max}.")


def _read_data(data_file_path: str) -> List[List[int]]:
    with open(data_file_path, "r") as file:
        lines = [x.strip() for x in file.readlines()]

    ret = []
    current_list = []
    for line in lines:
        if line:
            current_list.append(int(line))
        else:
            ret.append(current_list)
            current_list = []

    # Append the last list of integers.
    ret.append(current_list)

    return ret


if __name__ == "__main__":
    main()
