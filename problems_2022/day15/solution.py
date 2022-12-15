"""https://adventofcode.com/2022/day/15."""
import os
from typing import Tuple, List, Set
import re

import numpy as np

from adventofcode.util import read_lines_stripping_both_ends


# A (y, x) point.
_Point = Tuple[int, int]
# An interval.  Both left and right bounds are inclusive.
_Interval = Tuple[int, int]


def main():
    sensors_and_beacons = _read_data(data_file_path=os.path.join(os.path.dirname(__file__), "data.txt"))

    intervals, points_occupied = _row_impossible_intervals_and_beacon_points(
        row_index=2000000, sensors_and_beacons=sensors_and_beacons
    )
    num_impossible_positions = sum(x_max - x_min + 1 for x_min, x_max in intervals) - len(points_occupied)
    print(f"Part 1: The number of impossible positions is {num_impossible_positions}.")

    only_possible_point = _only_possible_point(sensors_and_beacons=sensors_and_beacons)
    print(
        f"Part 2: The point is {only_possible_point}.  The tuning frequency is "
        f"{only_possible_point[1] * 4000000 + only_possible_point[0]}."
    )


def _read_data(data_file_path: str) -> List[Tuple[_Point, _Point]]:
    """Returns a list of (sensor_position, nearest_beacon_position) tuples."""
    ret = []
    pattern = r"Sensor at x=(-?[0-9]+), y=(-?[0-9]+): closest beacon is at x=(-?[0-9]+), y=(-?[0-9]+)"
    for line in read_lines_stripping_both_ends(file_path=data_file_path):
        nums = re.match(pattern=pattern, string=line).groups()
        nums = tuple(int(x) for x in nums)
        ret.append(((nums[1], nums[0]), (nums[3], nums[2])))
    return ret


def _row_impossible_intervals_and_beacon_points(
    row_index: int, sensors_and_beacons: List[Tuple[_Point, _Point]]
) -> Tuple[List[_Interval], Set[_Point]]:
    intervals = []
    points_occupied = set()

    for sensor_position, beacon_position in sensors_and_beacons:
        manhattan_distance = np.sum(np.abs(np.array(sensor_position) - np.array(beacon_position)))
        vertical_distance = np.abs(sensor_position[0] - row_index)
        horizontal_distance = manhattan_distance - vertical_distance

        if horizontal_distance < 0:
            # No intersection with the row.
            continue

        if beacon_position[0] == row_index:
            points_occupied.add(beacon_position)

        intervals.append((sensor_position[1] - horizontal_distance, sensor_position[1] + horizontal_distance))

    return _merge_intervals(intervals=intervals), points_occupied


def _merge_intervals(intervals: List[_Interval]) -> List[_Interval]:
    # Sort intervals based on the left bounds.
    intervals = list(sorted(intervals, key=lambda x: x[0]))
    ret = [intervals[0]]
    for interval in intervals[1:]:
        last_interval = ret[-1]
        if interval[0] - last_interval[1] <= 1:
            # The next interval's left bound connects with the last interval's right bound.  Merge them.
            ret[-1] = (last_interval[0], max(last_interval[1], interval[1]))
        else:
            # The two intervals are not connected.
            ret.append(interval)

    return ret


def _only_possible_point(sensors_and_beacons: List[Tuple[_Point, _Point]]) -> _Point:
    max_coordinate = 4000000
    for y in range(0, max_coordinate + 1):
        intervals, points_occupied = _row_impossible_intervals_and_beacon_points(
            row_index=y, sensors_and_beacons=sensors_and_beacons
        )
        for i in range(1, len(intervals)):
            # Only check the point to the left of the next interval, so the 0th interval can be skipped.
            if 0 <= intervals[i][0] - 1 <= max_coordinate:
                return y, intervals[i][0] - 1

            if intervals[i][1] >= max_coordinate:
                break

    raise RuntimeError("Did not find the only point!")


if __name__ == "__main__":
    main()
