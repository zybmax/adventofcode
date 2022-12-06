"""https://adventofcode.com/2022/day/6."""
import os
from typing import Generator, Iterable
from collections import deque


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
