"""https://adventofcode.com/2021/day/10"""
import os.path
from statistics import median
from typing import List


def _make_translation_table():
    open_chars = "([{<"
    close_chars = ")]}>"
    return str.maketrans(open_chars + close_chars, close_chars + open_chars)


_SWAP_DIRECTION_TABLE = _make_translation_table()


def main():
    lines = _read_data(data_file_path=os.path.join(os.path.dirname(__file__), "data.txt"))
    scores = [_check_line(line) for line in lines]
    print(median(x for x in scores if x > 0))


def _read_data(data_file_path: str) -> List[str]:
    with open(data_file_path, "r") as file:
        lines = file.readlines()

    return [line.lstrip().rstrip() for line in lines]


def _check_line(line) -> int:
    """Returns the penalty score for line."""
    scores_by_closing_char = {")": 1, "]": 2, "}": 3, ">": 4}

    stack = []
    for char in line:
        if char in "([{<":
            stack.append(char)
        elif char != _flip_bracket(stack.pop()):
            return 0

    # Calculate penalty score.
    score = 0
    for opening_char in reversed(stack):
        score *= 5
        score += scores_by_closing_char[_flip_bracket(opening_char)]
    return score


def _flip_bracket(char: str) -> str:
    """Returns the opposite bracket."""
    return char.translate(_SWAP_DIRECTION_TABLE)


if __name__ == "__main__":
    main()
