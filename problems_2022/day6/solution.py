"""https://adventofcode.com/2022/day/6."""
import os
from typing import List, Tuple, Generator, Iterable
from collections import deque


NUM_STACKS = 9


# The stack status is a list, where the 0th element corresponds to stack 1, the 1st element corresponds to stack 2, etc.
# Each element is a list of single-character strings, representing the loads from bottom to top.
StackStatus = List[List[str]]
# The move instructions is a list of (how_many, from_which, to_which) tuples.  `from_which` and `to_which` are 0-based
# integers representing stack indices.
MoveInstructions = List[Tuple[int, int, int]]


def main():
    characters = _read_data(data_file_path=os.path.join(os.path.dirname(__file__), "data.txt"))
    position = _find_position_first_n_consecutive_different_characters(characters=characters, num_consecutive=4) + 1
    print(f"Part 1: The 1-based position of the first 4 consecutive different characters is {position}.")

    # Need to recreate the generator.
    characters = _read_data(data_file_path=os.path.join(os.path.dirname(__file__), "data.txt"))
    position = _find_position_first_n_consecutive_different_characters(characters=characters, num_consecutive=14) + 1
    print(f"Part 2: The 1-based position of the first 14 consecutive different characters is {position}.")


def _read_data(data_file_path: str) -> Generator[str, None, None]:
    with open(data_file_path, "r") as file:
        for line in file:
            for char in line:
                yield char


def _find_position_first_n_consecutive_different_characters(characters: Iterable[str], num_consecutive: int) -> int:
    current_characters = deque(maxlen=num_consecutive)
    for i, char in enumerate(characters):
        current_characters.append(char)
        if len(set(current_characters)) == num_consecutive:
            return i

    raise RuntimeError(f"Unable to find four consecutive different characters!")


if __name__ == "__main__":
    main()
