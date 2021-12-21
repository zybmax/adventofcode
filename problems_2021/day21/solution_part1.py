"""https://adventofcode.com/2021/day/21."""


def main():
    game = _Game(6, 10, _DeterministicDice())
    print(game.num_rolls * game.score_of_losing_player)


class _DeterministicDice:
    def __init__(self) -> None:
        self._current_value = 1
        self._max_value = 100

    def roll(self) -> int:
        ret = self._current_value

        self._current_value += 1
        if self._current_value > self._max_value:
            self._reset()

        return ret

    def _reset(self) -> None:
        self._current_value = 1


class _Game:
    def __init__(self, position_1: int, position_2: int, dice: _DeterministicDice) -> None:
        self._max_position = 10
        self._positions = [position_1, position_2]
        self._scores = [0, 0]
        self._dice = dice
        self._num_dice_rolls = 0
        self._simulate()

    def _simulate(self):
        while True:
            for i in range(2):
                num_steps = sum(self._dice.roll() for _ in range(3))
                self._positions[i] = (self._positions[i] + num_steps - 1) % 10 + 1
                self._scores[i] += self._positions[i]
                self._num_dice_rolls += 3
                if self._scores[i] >= 1000:
                    return

    @property
    def num_rolls(self) -> int:
        return self._num_dice_rolls

    @property
    def score_of_losing_player(self) -> int:
        return min(self._scores)


if __name__ == "__main__":
    main()
