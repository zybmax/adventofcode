"""https://adventofcode.com/2021/day/6"""
import os
import os.path
from typing import List


def main():
    days_left_list = _read_data(
        data_file_path=os.path.join(os.path.dirname(__file__), "data.txt")
    )

    num_days = 256

    # Make a hashmap where keys are the number of days left and the values are the number of fish.
    counts_by_num_days = {x: 0 for x in range(9)}
    for days_left in days_left_list:
        counts_by_num_days[days_left] += 1

    for day in range(num_days):
        new_counts_by_num_days = {}
        for days_left in range(8, -1, -1):
            if days_left != 0:
                new_counts_by_num_days[days_left - 1] = counts_by_num_days[days_left]
            else:
                new_counts_by_num_days[8] = counts_by_num_days[days_left]
                new_counts_by_num_days[6] += counts_by_num_days[days_left]
        counts_by_num_days = new_counts_by_num_days

    print(sum(counts_by_num_days.values()))


def _read_data(data_file_path: str) -> List[int]:
    with open(data_file_path, "r") as file:
        line = file.readline()

    return [int(x) for x in line.lstrip().rstrip().split(",")]


if __name__ == "__main__":
    main()
