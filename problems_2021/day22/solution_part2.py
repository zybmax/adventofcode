"""https://adventofcode.com/2021/day/22."""
import functools
import itertools
import os.path
from operator import and_
from operator import mul
from typing import List
from typing import Optional
from typing import Tuple


# Interval with both sides inclusive.
_Interval = Tuple[int, int]
# A 3D interval is (y_interval, x_interval, z_interval).
_Interval3D = Tuple[_Interval, _Interval, _Interval]
# A step is defined as (to_turn_on, interval_tuple).
_Step = Tuple[bool, _Interval3D]


def main():
    steps = _read_data(data_file_path=os.path.join(os.path.dirname(__file__), "data.txt"))

    cuboid_collection = _CuboidCollection()
    for to_turn_on, interval_3d in steps:
        if to_turn_on:
            cuboid_collection.add(_Cuboid(interval_3d=interval_3d))
        else:
            cuboid_collection.subtract(_Cuboid(interval_3d=interval_3d))

    print(cuboid_collection.total_volume)


def _read_data(data_file_path: str) -> List[_Step]:
    """Returns a list of steps."""
    with open(data_file_path, "r") as file:
        lines = file.readlines()

    ret = []
    for line in lines:
        line = line.strip()
        if line.startswith("on"):
            to_turn_on = True
            line = line[len("on ") :]
        else:
            to_turn_on = False
            line = line[len("off ") :]

        # Remove "x=", "y=" or "z=" from each substring before splitting by "..".
        intervals = tuple(tuple(int(x) for x in substring[2:].split("..")) for substring in line.split(","))
        # Convert to y, x, z ordering to be consistent with numpy convention.
        intervals = (intervals[1], intervals[0], intervals[2])

        ret.append((to_turn_on, intervals))

    return ret


class _Cuboid:
    def __init__(self, interval_3d: _Interval3D) -> None:
        self._interval_3d = interval_3d

    @property
    def interval_3d(self) -> _Interval3D:
        return self._interval_3d

    def __sub__(self, other: "_Cuboid") -> "_CuboidCollection":
        """Returns a cuboid collection resulting from subtracting two cuboids.

        Subtraction is defined as removing the overlapping cuboid between `self` and `other` from `self`. This can
        possibly cause splitting of the cuboid into multiple cuboids. For example, consider removing a cuboid at one
        corner of a larger cuboid, which would result in 7 smaller cuboids.
        """
        # If the two cuboids do not overlap, the subtraction is simply the first cuboid.
        if not _Cuboid._intervals_3d_have_overlap(self.interval_3d, other.interval_3d):
            return _CuboidCollection([self])

        # If they do have overlap, we should break up each interval into multiple, and mark their "keep" status. For
        # the sub-cuboid where the "keep" status for all the dimensions are False, that sub-cuboid should be removed.
        cuboid_list = []
        for (interval_y, to_keep_y), (interval_x, to_keep_x), (interval_z, to_keep_z) in itertools.product(
            *[_Cuboid._interval_subtract(self.interval_3d[i], other.interval_3d[i]) for i in range(3)]
        ):
            # As long as one dimension's "to keep" is True, we should keep this cuboid.
            if to_keep_y or to_keep_x or to_keep_z:
                cuboid_list.append(_Cuboid(interval_3d=(interval_y, interval_x, interval_z)))
        return _CuboidCollection(cuboid_list)

    @staticmethod
    def _interval_subtract(first_interval: _Interval, second_interval: _Interval) -> List[Tuple[_Interval, bool]]:
        """Returns a list of (interval, to_keep) tuples resulting from subtracting two 1D intervals.

        Assumes that the two intervals have overlap.

        For example, substracting (1, 5) and (2, 4) will result in [((1, 1), True), ((2, 4), False), ((5, 5), True)].
        Depending on the status of partial or full overlap, the resulting number of intervals can be 1, 2 or 3.
        """
        # Use if/else instead of if ... return (without else) for stylistic clarity.
        if second_interval[0] <= first_interval[0]:
            if second_interval[1] < first_interval[1]:
                return [
                    ((first_interval[0], second_interval[1]), False),
                    ((second_interval[1] + 1, first_interval[1]), True),
                ]

            return [(first_interval, False)]

        # second_interval[0] > first_interval[0].
        if second_interval[1] < first_interval[1]:
            return [
                ((first_interval[0], second_interval[0] - 1), True),
                ((second_interval[0], second_interval[1]), False),
                ((second_interval[1] + 1, first_interval[1]), True),
            ]

        return [
            ((first_interval[0], second_interval[0] - 1), True),
            ((second_interval[0], first_interval[1]), False),
        ]

    @property
    def volume(self) -> int:
        return functools.reduce(mul, [max_coord - min_coord + 1 for min_coord, max_coord in self.interval_3d], 1)

    @staticmethod
    def _intervals_3d_have_overlap(first_interval_3d: _Interval3D, second_interval_3d: _Interval3D) -> bool:
        # Two 3D intervals have overlap if and only if they have overlap in every dimension.
        return functools.reduce(
            and_, [_Cuboid._intervals_have_overlap(x, y) for x, y in zip(first_interval_3d, second_interval_3d)], True
        )

    @staticmethod
    def _intervals_have_overlap(first_interval: _Interval, second_interval: _Interval) -> bool:
        return not (first_interval[0] > second_interval[1] or first_interval[1] < second_interval[0])


class _CuboidCollection:
    def __init__(self, cuboids: Optional[List[_Cuboid]] = None) -> None:
        self.cuboids: List[_Cuboid] = cuboids if cuboids is not None else []

    def add(self, cuboid: _Cuboid) -> None:
        """Adds a new cuboid to the collection and updates the stored cuboids."""
        self.subtract(cuboid)
        self.cuboids.append(cuboid)

    def subtract(self, cuboid: _Cuboid) -> None:
        """Subtracts a cuboid from the collection and updates the stored cuboids."""
        cuboids = []
        for existing_cuboid in self.cuboids:
            cuboids.extend((existing_cuboid - cuboid).cuboids)
        self.cuboids = cuboids

    @property
    def total_volume(self) -> int:
        return sum(x.volume for x in self.cuboids)


if __name__ == "__main__":
    main()
