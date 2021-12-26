"""https://adventofcode.com/2021/day/24.

In the MONAD program, for each individual digit, w is used to read the digit (so is always reset), and x and y are also
reset to 0. So only z's value depends on the status from the last digit.

A program is defined as the (program_type, coefficient `alpha`, coefficient `beta`).
If program_type == 0, the program always does z_new = 26 * z + w_i + alpha_i.
If program_type == 1, the program does:
  if z % 26 - alpha_i == w_i:
      z_new = z // 26
  else:
      z_new = 26 * (z // 26) + w_i + beta_i

There are in total 7 type-0 programs and 7 type-1 programs. To make the resulting z zero after passing through all the
programs, all type-1 programs must trigger the first branch (that is, `z % 26 - alpha_i == w_i` must be True). Because
w_i is a number between 1 and 9, there is at most a single w_i that satisfies the condition (and possibly no w_i can
satisfy the condition).
"""
from typing import Optional, Tuple
import functools


MODEL_NUM_LENGTH = 14

# A program is defined as the (program_type, coefficient `alpha`, coefficient `beta`).
Program = Tuple[int, int, Optional[int]]


PROGRAMS = [
    (0, 6, None),
    (0, 14, None),
    (0, 14, None),
    (1, -8, 10),
    (0, 9, None),
    (0, 12, None),
    (1, -11, 8),
    (1, -4, 13),
    (1, -15, 12),
    (0, 6, None),
    (0, 9, None),
    (1, -1, 15),
    (1, -8, 4),
    (1, -14, 10),
]


def main():
    print("Part 1: ", _find_extreme_number())
    print("Part 2: ", _find_extreme_number(largest=False))


@functools.lru_cache(maxsize=None)
def _find_extreme_number(digit_position: int = 0, z: int = 0, largest: bool = True) -> Optional[str]:
    if digit_position > 13:
        return ""

    if PROGRAMS[digit_position][0] == 0:
        digits_to_search = range(9, 0, -1) if largest else range(1, 10)
        for digit in digits_to_search:
            new_z = 26 * z + digit + PROGRAMS[digit_position][1]
            largest_remaining = _find_extreme_number(digit_position=digit_position + 1, z=new_z, largest=largest)
            if largest_remaining is None:
                continue

            return str(digit) + largest_remaining

        # None of digits 1-9 can return a valid result.
        return None

    # The current program is type 1.
    digit = z % 26 + PROGRAMS[digit_position][1]
    if not 1 <= digit <= 9:
        # No valid w exists.
        return None

    new_z = z // 26
    largest_remaining = _find_extreme_number(digit_position=digit_position + 1, z=new_z, largest=largest)
    return str(digit) + largest_remaining if largest_remaining is not None else None


if __name__ == "__main__":
    main()
