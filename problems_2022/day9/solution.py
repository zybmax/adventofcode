"""https://adventofcode.com/2022/day/9."""
import os
from typing import Tuple, List

import numpy as np

from adventofcode.util import read_lines_stripping_both_ends


# The (y, x) position.  The positive direction for y is downward.
_Position = Tuple[int, int]
# The direction (e.g., "R" for right) and the number of steps (e.g., 4).
_Instruction = Tuple[str, int]


def main():
    instructions = _read_data(data_file_path=os.path.join(os.path.dirname(__file__), "data.txt"))

    tail_positions = _tail_positions(start_position=(0, 0), instructions=instructions, num_knots=2)
    print(f"Part 1: The number of unique tail positions is {len(set(tail_positions))}.")

    tail_positions = _tail_positions(start_position=(0, 0), instructions=instructions, num_knots=10)
    print(f"Part 2: The number of unique tail positions is {len(set(tail_positions))}.")


def _read_data(data_file_path: str) -> List[_Instruction]:
    ret = []
    for line in read_lines_stripping_both_ends(file_path=data_file_path):
        direction, num_steps = line.split(" ")
        num_steps = int(num_steps)
        ret.append((direction, num_steps))

    return ret


def _tail_positions(start_position: _Position, instructions: List[_Instruction], num_knots: int) -> List[_Position]:
    """Returns the list of tail positions all steps, for a rope with `num_knots` knots."""
    knot_positions = [np.array(start_position, dtype=int) for _ in range(num_knots)]

    ret = []
    for direction, num_steps in instructions:
        for _ in range(num_steps):
            # The head position simply follows the instruction.
            head_position = knot_positions[0]
            if direction == "R":
                head_position[1] += 1
            elif direction == "L":
                head_position[1] -= 1
            elif direction == "U":
                # Use convention that going down is +1, and going up is -1.
                head_position[0] -= 1
            elif direction == "D":
                head_position[0] += 1

            # Recursively find the next knot's position based on the previous knot's position.
            for knot_index in range(1, num_knots):
                previous_knot_position = knot_positions[knot_index - 1]
                knot_position = knot_positions[knot_index]
                # Only need to move if in at least one of the axes, the distance is 2.
                if np.max(np.abs(previous_knot_position - knot_position)) > 1:
                    axes_with_distance_2 = np.where(np.abs(previous_knot_position - knot_position) == 2)[0]
                    for axis in range(2):
                        if axis in axes_with_distance_2:
                            # Move the current knot 1 step towards the previous knot, which is equivalent to moving the
                            # current knot to the middle point between the current knot and previous knot.
                            knot_position[axis] = int((knot_position[axis] + previous_knot_position[axis]) / 2)
                        else:
                            knot_position[axis] = previous_knot_position[axis]

            ret.append(tuple(int(x) for x in knot_positions[-1]))

    return ret


if __name__ == "__main__":
    main()
