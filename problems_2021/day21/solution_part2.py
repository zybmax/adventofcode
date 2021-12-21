"""https://adventofcode.com/2021/day/21."""
import itertools
import functools
from typing import Tuple, Dict
from collections import Counter


# A player status is defined as the current position and the current score.
_PlayerStatus = Tuple[int, int]
_GameStatus = Tuple[_PlayerStatus, _PlayerStatus]

_WINNING_SCORE = 21


def main():
    print(max(_nums_win(game_status=((6, 0), (10, 0)))))


@functools.lru_cache(maxsize=None)
def _nums_win(game_status: _GameStatus) -> Tuple[int, int]:
    """Returns the numbers of win situations for players 0 and 1.

    The next player to go is always the 0th player.

    If the current score plus some of the possible scores exceed the winning score, add those to the ret, then flip
    the players and calculate the nums of wins in the rest of the cases.
    """
    num_win_0 = num_win_1 = 0
    for dice_sum, frequency in _three_roll_sum_frequencies().items():
        new_position_0 = (game_status[0][0] + dice_sum - 1) % 10 + 1
        new_score_0 = game_status[0][1] + new_position_0
        if new_score_0 >= _WINNING_SCORE:
            num_win_0 += frequency
        else:
            # Flip the player status to reduce the number of possible scenarios, and note that the output should also
            # be flipped.
            new_game_status = (game_status[1], (new_position_0, new_score_0))
            conditional_num_win_1, conditional_num_win_0 = _nums_win(new_game_status)
            num_win_0 += conditional_num_win_0 * frequency
            num_win_1 += conditional_num_win_1 * frequency

    return num_win_0, num_win_1


@functools.lru_cache(maxsize=1)
def _three_roll_sum_frequencies() -> Dict[int, int]:
    """Returns a dict where the keys are the sum of three dice rolls and the values are the frequencies."""
    ret = Counter()
    for i, j, k in itertools.product(range(1, 4), range(1, 4), range(1, 4)):
        ret[i + j + k] += 1
    return dict(ret)


if __name__ == "__main__":
    main()
