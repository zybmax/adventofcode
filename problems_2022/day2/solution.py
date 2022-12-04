"""https://adventofcode.com/2022/day/1."""
import os
from typing import List, Tuple

from adventofcode.util import read_lines_stripping_both_ends


# The mapping between the action as a letter to the numeric label.
ROCK_PAPER_SCISSOR_MAPPING = {"A": 1, "B": 2, "C": 3, "X": 1, "Y": 2, "Z": 3}
# Win is denoted as 1; draw as 0; lose as -1.  The values are the corresponding scores.
WIN_LOSE_SCORE_MAPPING = {-1: 0, 0: 3, 1: 6}


def main():
    inputs = _read_data(data_file_path=os.path.join(os.path.dirname(__file__), "data.txt"))
    total_score = sum(_score(opponent_input=x, my_input=y) for x, y in inputs)
    print(f"Problem 1: Total score is {total_score}.")

    total_score = sum(_score_based_on_win_lose(opponent_input=x, win_lose=y - 2) for x, y in inputs)
    print(f"Problem 2: Total score is {total_score}.")


def _read_data(data_file_path: str) -> List[Tuple[int, int]]:
    lines = read_lines_stripping_both_ends(file_path=data_file_path)

    ret = []
    for line in lines:
        ret.append(tuple(ROCK_PAPER_SCISSOR_MAPPING[x] for x in line.split(sep=" ")))

    return ret


def _score(opponent_input: int, my_input: int) -> int:
    return my_input + WIN_LOSE_SCORE_MAPPING[_win_lose(opponent_input=opponent_input, my_input=my_input)]


def _win_lose(opponent_input: int, my_input: int) -> int:
    """Returns 1 if win, -1 if lose, 0 if draw."""
    if opponent_input == my_input:
        return 0

    if (opponent_input - my_input) % 3 == 2:
        return 1

    return -1


def _score_based_on_win_lose(opponent_input: int, win_lose: int) -> int:
    """Returns the score of a round based on the opponent input and whether I should win/draw/lose."""
    if win_lose == 0:
        my_input = opponent_input
    elif win_lose == 1:
        my_input = opponent_input % 3 + 1
    else:
        my_input = (opponent_input - 2) % 3 + 1

    return my_input + WIN_LOSE_SCORE_MAPPING[win_lose]


if __name__ == "__main__":
    main()
