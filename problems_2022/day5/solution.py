"""https://adventofcode.com/2022/day/5."""
import copy
import os
import re
from typing import List, Tuple

from adventofcode.util import read_lines_stripping_both_ends

NUM_STACKS = 9


# The stack status is a list, where the 0th element corresponds to stack 1, the 1st element corresponds to stack 2, etc.
# Each element is a list of single-character strings, representing the loads from bottom to top.
StackStatus = List[List[str]]
# The move instructions is a list of (how_many, from_which, to_which) tuples.  `from_which` and `to_which` are 0-based
# integers representing stack indices.
MoveInstructions = List[Tuple[int, int, int]]


def main():
    stack_status, move_instructions = _read_data(data_file_path=os.path.join(os.path.dirname(__file__), "data.txt"))

    print("Stack status:", stack_status)
    print("Move instructions: ", move_instructions)

    work_stack_status = copy.deepcopy(stack_status)
    for num_moves, source, destination in move_instructions:
        for _ in range(num_moves):
            element = work_stack_status[source].pop()
            work_stack_status[destination].append(element)

    print(f"Part 1: The top elements are {_top_elements(stack_status=work_stack_status)}.")

    work_stack_status = copy.deepcopy(stack_status)
    for num_moves, source, destination in move_instructions:
        elements = work_stack_status[source][-num_moves:]
        work_stack_status[source] = work_stack_status[source][:-num_moves]
        work_stack_status[destination].extend(elements)

    print(f"Part 2: The top elements are {_top_elements(stack_status=work_stack_status)}.")


def _read_data(data_file_path: str) -> Tuple[StackStatus, MoveInstructions]:
    """Returns the stack status and move instructions."""
    lines = read_lines_stripping_both_ends(file_path=data_file_path)

    # Break the inputs into two parts: the stack status and the move instructions.
    empty_line_index = lines.index("")
    stack_status_lines = lines[:empty_line_index]
    move_instructions_lines = lines[empty_line_index + 1 :]

    # Parse the stack status.
    stack_status = []
    max_height = len(stack_status_lines) - 1
    for stack_index in range(NUM_STACKS):
        stack = []
        for height_index in range(max_height):
            try:
                # The corresponding letter for each stack is at the `1 + stack_index * 4` position.
                char = lines[max_height - height_index - 1][1 + stack_index * 4]
            except IndexError:
                # Exceeded stack top.  Break.
                break

            if char == " ":
                # Also exceeded stack top.  Break.
                break

            stack.append(char)

        stack_status.append(stack)

    # Parse the move instructions.
    move_instructions = []
    for line in move_instructions_lines:
        num_moves, source, destination = re.search(r"move ([0-9]+) from ([0-9]+) to ([0-9]+)", line).groups()
        move_instructions.append((int(num_moves), int(source) - 1, int(destination) - 1))

    return stack_status, move_instructions


def _top_elements(stack_status: StackStatus) -> str:
    return "".join(stack[-1] for stack in stack_status)


if __name__ == "__main__":
    main()
