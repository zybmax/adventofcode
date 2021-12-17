"""https://adventofcode.com/2021/day/17.

x(n) = (vx - (n - 1) / 2) * n if n < vx else vx * (vx + 1) / 2.
y(n) = (vy - (n - 1) / 2) * n.

Assume that the target field for x is positive and the target field for y is negative, which is satisfied by the test
input.

The valid range for vx is:
- vx <= x_max, because otherwise the first step goes over the target field.
- vx * (vx + 1) / 2 >= x_min, otherwise it will never reach the target field in the x direction. This gives us:
  vx >= ceil(-1 / 2 + sqrt(2 * x_min)).

Another useful fact to observe is that when vy is positive, after 2 * vy steps, it will come back to zero, and the
(2 * vy + 1)th step's y velocity is -vy - 1.
When vy is positive, the necessary condition for vy is -vy - 1 >= y_min -> vy <= -y_min - 1.
When vy is negative, the necessary condition for vy is vy >= y_min.
Combining both, we have y_min <= vy <= -y_min - 1.

Instead of doing a 2D search (brute-force), we have do two 1D searches, one for x and one for y:
- First find out which vx can reach the target field in the x direction. Take down the vx, as well as the (n_x_min,
n_x_max) for each vx.
- Then find out which vy can reach the target field in the y direction and calculate the (n_y_min, n_y_max) for each vy.
Look at all feasible vx's and find the intersection of the n intervals.
"""
import itertools
import math
import os.path
from typing import Optional
from typing import Tuple
from typing import Union


# Closed interval, containing both the left and right boundaries. Use float only for infinity. Only the right boundary
# supports infinity.
_Interval = Tuple[int, Union[int, float]]


def main():
    x_interval, y_interval = _read_data(data_file_path=os.path.join(os.path.dirname(__file__), "data.txt"))

    feasible_vx_interval = _find_feasible_vx_interval(x_interval=x_interval)
    n_intervals_by_vx = {}
    for vx in range(feasible_vx_interval[0], feasible_vx_interval[1] + 1):
        n_interval = _find_n_interval_in_x(vx=vx, x_interval=x_interval)
        if n_interval is not None:
            n_intervals_by_vx[vx] = n_interval

    feasible_vy_interval = _find_feasible_vy_interval(y_interval=y_interval)
    n_intervals_by_vy = {}
    for vy in range(feasible_vy_interval[0], feasible_vy_interval[1] + 1):
        n_interval = _find_n_interval_in_y(vy=vy, y_interval=y_interval)
        if n_interval is not None:
            n_intervals_by_vy[vy] = n_interval

    # Find all vx, vy pairs.
    vxs_and_vys = []
    for vx, vy in itertools.product(n_intervals_by_vx, n_intervals_by_vy):
        # If the n intervals overlap between x and y, there must be at least an `n` that causes both x and y to be in
        # the target field.
        if _intervals_have_overlap(n_intervals_by_vx[vx], n_intervals_by_vy[vy]):
            vxs_and_vys.append((vx, vy))

    # Part 1.
    print(max(_highest_y(vy) for vy in set(vy_ for vx_, vy_ in vxs_and_vys)))

    # Part 2
    print(len(vxs_and_vys))


def _read_data(data_file_path: str) -> Tuple[_Interval, _Interval]:
    """Returns the risk level map."""
    with open(data_file_path, "r") as file:
        line = file.readline().lstrip().rstrip()

    line = line[len("target area: ") :]
    xy_parts = line.split(", ")
    ret = ()
    for part in xy_parts:
        # Remove "x=" or "y=".
        part = part[2:]
        ret = ret + (tuple(int(x) for x in part.split("..")),)

    return ret


def _x_position(vx, n) -> int:
    """Returns the x position with initial velocity `vx` after step `n`."""
    return int((vx - (n - 1) / 2) * n) if n < vx else int(vx * (vx + 1) / 2)


def _y_position(vy, n) -> int:
    """Returns the y position with initial velocity `vy` after step `n`."""
    return int((vy - (n - 1) / 2) * n)


def _highest_y(vy) -> int:
    """Returns the highest height in the trajectory for initial y velocity `vy`."""
    return int(vy * (vy + 1) / 2) if vy > 0 else 0


def _find_feasible_vx_interval(x_interval: _Interval) -> _Interval:
    """Returns the feasible `vx` interval based on the target field interval in the x direction."""
    return math.ceil(-0.5 + math.sqrt(2 * x_interval[0])), x_interval[1]


def _find_feasible_vy_interval(y_interval: _Interval) -> _Interval:
    """Returns the feasible `vy` interval based on the target field interval in the y direction."""
    return y_interval[0], -y_interval[0] - 1


def _find_n_interval_in_x(vx: int, x_interval: _Interval) -> Optional[_Interval]:
    """Returns the interval for n (step) for the x coordinate to be in the target field.

    Returns None if no `n` satisfies the criterion.
    """
    # The x coordinate will never reach the target field.
    final_x = _x_position(vx=vx, n=vx)
    if final_x < x_interval[0]:
        return None

    # Analytically find the first n that causes the x position to be at least x_interval[0]. This involves solving the
    # inequality `_x_position(vx, n) >= x_interval[0]`. The smaller root should be picked because only left half of the
    # parabola is valid before reaching the maximum at `n=vx`.
    return _find_n_interval(v=vx, interval=x_interval, increasing=True)


def _find_n_interval_in_y(vy: int, y_interval: _Interval) -> Optional[_Interval]:
    """Returns the interval for n (step) for the y coordinate to be in the target field.

    Returns None if no `n` satisfies the criterion.
    """
    # Analytically find the n interval that causes the y position to be within y_interval. Choose the root on the right
    # because the parabola (with its opening facing downward) is decreasing when it reaches the y target field
    # (negative).
    return _find_n_interval(v=vy, interval=y_interval, increasing=False)


def _find_n_interval(v: int, interval: _Interval, increasing: bool) -> Optional[_Interval]:
    """Returns the n interval that causes the position to be within the interval.

    Returns None if no `n` satisfies the criterion.

    The position is related to v and n by position = (v - (n - 1) / 2) * n.
    `increasing` should be True if the position is increasing when reaching the target interval and False otherwise.
    """
    factor = -1 if increasing else 1
    interval = interval if increasing else tuple(reversed(interval))

    n_start = math.ceil((1 + 2 * v + factor * math.sqrt((1 + 2 * v) ** 2 - 8 * interval[0])) / 2)
    try:
        n_end = math.floor((1 + 2 * v + factor * math.sqrt((1 + 2 * v) ** 2 - 8 * interval[1])) / 2)
    except ValueError:
        n_end = float("inf")

    return None if n_end < n_start else (n_start, n_end)


def _intervals_have_overlap(interval_1: _Interval, interval_2: _Interval) -> bool:
    return not (interval_1[0] > interval_2[1] or interval_2[0] > interval_1[1])


if __name__ == "__main__":
    main()
