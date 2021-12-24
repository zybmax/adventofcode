"""https://adventofcode.com/2021/day/23."""
import functools
from typing import List
from typing import Set
from typing import Tuple


# An amphipod is represented by its type (0 for A, 1 for B, ...) and the individual ID within its type (0 or 1).
_Amphipod = Tuple[int, int]
# Position is defined by the (row_idx, col_idx) in the map.  Many positions are forbidden.
_Position = Tuple[int, int]
# The game status is the statuses of all amphipods. Each status is its position and whether it has reached its home.
_GameStatus = Tuple[Tuple[_Amphipod, _Position, bool], ...]
# A move is a (amphipod, start_position, end_position) tuple.
_Move = Tuple[_Amphipod, _Position, _Position]


_HOME_COLUMNS_BY_AMPHIPOD_TYPE = {0: 2, 1: 4, 2: 6, 3: 8}
_HALLWAY_VALID_X_POSITIONS = {0, 1, 3, 5, 7, 9, 10}


_EXAMPLE_START_STATUS = (
    ((0, 0), (4, 2), True),
    ((0, 1), (3, 6), False),
    ((0, 2), (2, 8), False),
    ((0, 3), (4, 8), False),
    ((1, 0), (1, 2), False),
    ((1, 1), (3, 4), False),
    ((1, 2), (1, 6), False),
    ((1, 3), (2, 6), False),
    ((2, 0), (1, 4), False),
    ((2, 1), (2, 4), False),
    ((2, 2), (4, 6), True),
    ((2, 3), (3, 8), False),
    ((3, 0), (2, 2), False),
    ((3, 1), (3, 2), False),
    ((3, 2), (4, 4), False),
    ((3, 3), (1, 8), False),
)

_TEST_START_STATUS = (
    ((0, 0), (4, 6), False),
    ((0, 1), (4, 8), False),
    ((0, 2), (3, 6), False),
    ((0, 3), (2, 8), False),
    ((1, 0), (1, 2), False),
    ((1, 1), (1, 8), False),
    ((1, 2), (3, 4), False),
    ((1, 3), (2, 6), False),
    ((2, 0), (1, 4), False),
    ((2, 1), (1, 6), False),
    ((2, 2), (2, 4), False),
    ((2, 3), (3, 8), False),
    ((3, 0), (4, 2), False),
    ((3, 1), (4, 4), False),
    ((3, 2), (2, 2), False),
    ((3, 3), (3, 2), False),
)

_ROOM_DEPTH = 4


def main():
    print(lowest_cost(game_status=_TEST_START_STATUS))


@functools.lru_cache(maxsize=None)
def lowest_cost(game_status: _GameStatus) -> Tuple[int, List[Tuple[_Amphipod, _Position, _Position]]]:
    """Returns the lowest cost if the game is to start from the current game status and the moves."""
    if all(at_home for _, _, at_home in game_status):
        return 0, []

    all_amphipod_positions = set(position for _, position, _ in game_status)
    available_hallway_positions = set((0, x) for x in _HALLWAY_VALID_X_POSITIONS) - all_amphipod_positions

    min_cost = float("inf")
    moves = None

    for amphipod, position, at_home in game_status:
        if at_home:
            # That amphipod has already reached home and will not move again.
            continue

        if position[0] == 0:
            # If this amphipod's current position is the top row, the next valid move must be to move back to the
            # deepest available space in its home. However, if the deeper space in the home is occupied by a wrong-
            # type amphipod, then the move is not valid.
            home_column = _HOME_COLUMNS_BY_AMPHIPOD_TYPE[amphipod[0]]
            new_position = (
                _ROOM_DEPTH - _num_correct_typed_amphipods_at_bottom_of_room(game_status, amphipod_type=amphipod[0]),
                home_column,
            )
            if _move_is_blocked(
                all_amphipod_positions=all_amphipod_positions, start_position=position, end_position=new_position
            ):
                continue

            new_game_status = ()
            for amphipod_, position_, at_home_ in game_status:
                if amphipod_ == amphipod:
                    new_game_status = new_game_status + ((amphipod_, new_position, True),)
                else:
                    new_game_status = new_game_status + ((amphipod_, position_, at_home_),)

            cost_of_move = _cost_of_move(amphipod_type=amphipod[0], start_position=position, end_position=new_position)
            remaining_cost, remaining_moves = lowest_cost(new_game_status)
            if cost_of_move + remaining_cost < min_cost:
                min_cost = cost_of_move + remaining_cost
                moves = [(amphipod, position, new_position)] + remaining_moves
            continue

        # The current amphipod is at its start position and the next move must be to move out to the hallway.
        for new_position in available_hallway_positions:
            if _move_is_blocked(
                all_amphipod_positions=all_amphipod_positions, start_position=position, end_position=new_position
            ):
                continue

            new_game_status = ()
            for amphipod_, position_, at_home_ in game_status:
                if amphipod_ == amphipod:
                    new_game_status = new_game_status + ((amphipod_, new_position, False),)
                else:
                    new_game_status = new_game_status + ((amphipod_, position_, at_home_),)

            cost_of_move = _cost_of_move(amphipod_type=amphipod[0], start_position=position, end_position=new_position)
            remaining_cost, remaining_moves = lowest_cost(new_game_status)
            if cost_of_move + remaining_cost < min_cost:
                min_cost = cost_of_move + remaining_cost
                moves = [(amphipod, position, new_position)] + remaining_moves

    return min_cost, moves


def _num_correct_typed_amphipods_at_bottom_of_room(game_status: _GameStatus, amphipod_type: int) -> int:
    same_type_positions = set(position for (type_, _), position, _ in game_status if type_ == amphipod_type)
    num = 0
    for depth in range(4, 0, -1):
        if (depth, _HOME_COLUMNS_BY_AMPHIPOD_TYPE[amphipod_type]) not in same_type_positions:
            return num

        # The current depth is occupied by the correct-typed amphibian. Add 1.
        num += 1

    # All four positions are occupied.
    return num


def _move_is_blocked(
    all_amphipod_positions: Set[_Position], start_position: _Position, end_position: _Position
) -> bool:
    other_amphipod_positions = all_amphipod_positions - {start_position}
    # The end position must not be occupied no matter what.
    if end_position in other_amphipod_positions:
        return True

    # Reorder start_position and end_position so that end_position is always in a room.
    if end_position[0] == 0:
        start_position, end_position = end_position, start_position
    # If moving out from or into the deeper space in the room, then the shallower part of the room must not be occupied.
    for shallower_y in range(end_position[0] - 1, 0, -1):
        if (shallower_y, end_position[1]) in other_amphipod_positions:
            return True

    # Make sure that the hallway is not blocked for the move.
    hallway_valid_positions_on_path = set(
        (0, i)
        for i in range(min(start_position[1], end_position[1]), max(start_position[1], end_position[1]) + 1)
        if i in _HALLWAY_VALID_X_POSITIONS
    )
    if len(hallway_valid_positions_on_path.intersection(other_amphipod_positions)) > 0:
        return True

    # No hallway blockage and no room blockage, the move is not blocked.
    return False


def _cost_of_move(amphipod_type: int, start_position: _Position, end_position: _Position):
    unit_cost = {0: 1, 1: 10, 2: 100, 3: 1000}[amphipod_type]
    return unit_cost * (abs(start_position[1] - end_position[1]) + abs(start_position[0] - end_position[0]))


if __name__ == "__main__":
    main()
