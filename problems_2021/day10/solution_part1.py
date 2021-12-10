"""https://adventofcode.com/2021/day/10"""
import os.path
from typing import List


def _make_translation_table():
    open_chars = "([{<"
    close_chars = ")]}>"
    return str.maketrans(open_chars + close_chars, close_chars + open_chars)


_SWAP_DIRECTION_TABLE = _make_translation_table()


def main():
    lines = _read_data(
        data_file_path=os.path.join(os.path.dirname(__file__), "data.txt")
    )

    print(sum(_check_line(line) for line in lines))


def _read_data(data_file_path: str) -> List[str]:
    with open(data_file_path, "r") as file:
        lines = file.readlines()

    return [line.lstrip().rstrip() for line in lines]


def _check_line(line) -> int:
    """Returns the penalty score for line."""
    scores_by_closing_char = {")": 3, "]": 57, "}": 1197, ">": 25137}
    stack = []
    for char in line:
        if char in "([{<":
            stack.append(char)
        elif char != _flip_bracket(stack.pop()):
            return scores_by_closing_char[char]

    # No corruption found.
    return 0


def _flip_bracket(char: str) -> str:
    """Returns the opposite bracket."""
    return char.translate(_SWAP_DIRECTION_TABLE)


if __name__ == "__main__":
    main()
