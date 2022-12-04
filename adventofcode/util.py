"""Utilities for solving Advent of Code problems."""
from typing import List


def read_lines_stripping_both_ends(file_path: str) -> List[str]:
    """Returns a list of strings representing the lines in the input file, stripped at both ends."""
    with open(file_path, "r") as file:
        return [x.strip() for x in file.readlines()]
