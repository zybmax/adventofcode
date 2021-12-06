"""https://adventofcode.com/2021/day/4#part2"""
import os
import os.path
from typing import List, Tuple
import itertools

import numpy as np


def main():
    order, boards = _read_data(
        data_file_path=os.path.join(os.path.dirname(__file__), "data.txt")
    )

    boards_already_won = [False] * len(boards)
    num_boards_left = len(boards)
    found = False

    for num_called in order:
        for i, board in enumerate(boards):
            if boards_already_won[i]:
                continue

            board.register_num(num_called)
            if board.bingo:
                boards_already_won[i] = True
                num_boards_left -= 1

                if num_boards_left == 0:
                    last_board = board
                    last_num = num_called
                    found = True
                    break

        if found:
            break

    # Include the last number.
    result = last_board.remaining * last_num
    print(f"Result is {result}.")


def _read_data(data_file_path: str) -> Tuple[List[int], List["Board"]]:
    with open(data_file_path, "r") as file:
        first_line = file.readline().rstrip()
        order = [int(x) for x in first_line.split(",")]

        # Read 6 lines at a time.
        boards = []

        next_line = file.readline()
        while next_line:
            next_lines = [file.readline().rstrip().lstrip() for i in range(5)]
            board = np.zeros((5, 5), dtype=int)
            for row_index, row in enumerate(next_lines):
                board[row_index, :] = [int(x) for x in row.split()]

            print()
            print(board)

            boards.append(Board(board))

            next_line = file.readline()

    return order, boards


class Board:
    def __init__(self, board: np.ndarray):
        self.remaining = np.sum(board)

        self._coordinates = {}
        for i, j in itertools.product(range(5), range(5)):
            self._coordinates[board[i, j]] = (i, j)

        self._nums_called_rows = [0] * 5
        self._nums_called_cols = [0] * 5

        self.bingo = False

    def _coordinate(self, value):
        """Returns the (i, j) coordinate corresponding to input value."""
        return self._coordinates[value]

    def register_num(self, num: int):
        try:
            i, j = self._coordinate(num)
        except KeyError:
            return

        self.remaining -= num

        self._nums_called_cols[j] += 1
        if self._nums_called_cols[j] == 5:
            self.bingo = True

        self._nums_called_rows[i] += 1
        if self._nums_called_rows[i] == 5:
            self.bingo = True


if __name__ == "__main__":
    main()
