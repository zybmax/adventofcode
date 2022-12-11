"""https://adventofcode.com/2022/day/11."""
from typing import List, Callable

import numpy as np


class Monkey:
    def __init__(
        self,
        starting_items: List[int],
        operation: Callable[[int], int],
        test: Callable[[int], bool],
        idx_to_throw_to_if_true: int,
        idx_to_thow_to_if_false: int,
    ) -> None:
        self.items = starting_items
        self.operation = operation
        self.test = test
        self.idx_to_thow_to_if_true = idx_to_throw_to_if_true
        self.idx_to_throw_to_if_false = idx_to_thow_to_if_false


def initialize_monkeys() -> List[Monkey]:
    return [
        Monkey(
            starting_items=[66, 59, 64, 51],
            operation=lambda x: x * 3,
            test=lambda x: x % 2 == 0,
            idx_to_throw_to_if_true=1,
            idx_to_thow_to_if_false=4,
        ),
        Monkey(
            starting_items=[67, 61],
            operation=lambda x: x * 19,
            test=lambda x: x % 7 == 0,
            idx_to_throw_to_if_true=3,
            idx_to_thow_to_if_false=5,
        ),
        Monkey(
            starting_items=[86, 93, 80, 70, 71, 81, 56],
            operation=lambda x: x + 2,
            test=lambda x: x % 11 == 0,
            idx_to_throw_to_if_true=4,
            idx_to_thow_to_if_false=0,
        ),
        Monkey(
            starting_items=[94],
            operation=lambda x: x**2,
            test=lambda x: x % 19 == 0,
            idx_to_throw_to_if_true=7,
            idx_to_thow_to_if_false=6,
        ),
        Monkey(
            starting_items=[71, 92, 64],
            operation=lambda x: x + 8,
            test=lambda x: x % 3 == 0,
            idx_to_throw_to_if_true=5,
            idx_to_thow_to_if_false=1,
        ),
        Monkey(
            starting_items=[58, 81, 92, 75, 56],
            operation=lambda x: x + 6,
            test=lambda x: x % 5 == 0,
            idx_to_throw_to_if_true=3,
            idx_to_thow_to_if_false=6,
        ),
        Monkey(
            starting_items=[82, 98, 77, 94, 86, 81],
            operation=lambda x: x + 7,
            test=lambda x: x % 17 == 0,
            idx_to_throw_to_if_true=7,
            idx_to_thow_to_if_false=2,
        ),
        Monkey(
            starting_items=[54, 95, 70, 93, 88, 93, 63, 50],
            operation=lambda x: x + 4,
            test=lambda x: x % 13 == 0,
            idx_to_throw_to_if_true=2,
            idx_to_thow_to_if_false=0,
        ),
    ]


# The test is always to check whether the item is divisible by a prime number.  We can compute the modulus of all the
# item values against the least common multiple of the prime numbers, and get the same "throw to" decisions, under the
# operations (adding a constant, multiplication by a constant, and squaring).
LEAST_COMMON_MULTIPLE = 2 * 7 * 11 * 19 * 3 * 5 * 17 * 13


def main():
    monkeys = initialize_monkeys()
    nums = nums_of_inspections(monkeys=monkeys, num_rounds=20, divide_by=3)
    monkey_business = np.prod(list(sorted(nums, reverse=True))[:2]).item()
    print(f"Part 1: The monkey business is {monkey_business}.")

    monkeys = initialize_monkeys()
    nums = nums_of_inspections(monkeys=monkeys, num_rounds=10000)
    monkey_business = np.prod(list(sorted(nums, reverse=True))[:2]).item()
    print(f"Part 2: The monkey business is {monkey_business}.")


def nums_of_inspections(monkeys: List[Monkey], num_rounds: int, divide_by: int = 1) -> List[int]:
    ret = [0] * len(monkeys)

    for round_idx in range(num_rounds):
        for monkey_idx, monkey in enumerate(monkeys):
            num_items = len(monkey.items)
            for item_idx in range(num_items):
                ret[monkey_idx] += 1
                item = monkey.items.pop(0)
                item = (monkey.operation(item) // divide_by) % LEAST_COMMON_MULTIPLE
                idx_to_throw_to = (
                    monkey.idx_to_thow_to_if_true if monkey.test(item) else monkey.idx_to_throw_to_if_false
                )
                monkeys[idx_to_throw_to].items.append(item)

    return ret


if __name__ == "__main__":
    main()
