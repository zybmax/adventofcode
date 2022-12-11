"""https://adventofcode.com/2022/day/10."""
import os
from typing import List, Optional

from adventofcode.util import read_lines_stripping_both_ends


def main():
    instructions = _read_data(data_file_path=os.path.join(os.path.dirname(__file__), "data.txt"))

    positions = _simulate_positions(instructions=instructions)
    # The cycle indices are 1-based.
    cycle_indices = list(range(20, 221, 40))
    sum_of_strengths = sum(positions[cycle_index - 1] * cycle_index for cycle_index in cycle_indices)
    print(f"Part 1: The sum of strengths at cycles {cycle_indices} is {sum_of_strengths}.")

    pattern = _compute_pattern(positions=positions)
    print(f"Part 2: The pattern is ")
    for line in pattern:
        print(line)


def _read_data(data_file_path: str) -> List[Optional[int]]:
    """Returns instructions as a list of integers; None values indicate "noop"."""
    ret = []
    for line in read_lines_stripping_both_ends(file_path=data_file_path):
        if line == "noop":
            ret.append(None)
        else:
            ret.append(int(line.split(" ")[1]))

    return ret


def _simulate_positions(instructions: List[Optional[int]]) -> List[int]:
    """Returns the positions at all steps."""
    position = 1
    ret = [position]

    for instruction in instructions:
        if instruction is None:
            # Do nothing.
            ret.append(position)
            continue

        ret.append(position)
        position = position + instruction
        ret.append(position)

    return ret


def _compute_pattern(positions: List[int]) -> List[str]:
    """Returns the rows of the patterns, with "#" representing dark pixels and "." representing lit pixels."""
    letters = []
    line_length = 40
    num_letters = 240
    for i in range(num_letters):
        y, x = i // line_length, i % line_length
        if positions[i] - 1 <= x <= positions[i] + 1:
            letters.append(".")
        else:
            letters.append("#")

    ret = []
    num_lines = num_letters // line_length
    for y_idx in range(num_lines):
        ret.append("".join(letters[y_idx * line_length : (y_idx + 1) * line_length]))
    return ret


if __name__ == "__main__":
    main()
