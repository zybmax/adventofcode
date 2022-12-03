"""https://adventofcode.com/2021/day/8"""
import os.path
import re
from typing import Dict, TypeAlias
from typing import List
from typing import Tuple


# A code is the numerical representation (e.g., [2, 5]) of a string (e.g., "cf") representing a single digit. A code
# is order-insensitive. A code is made up of several code nums (e.g., 2 and 5).
_Code: TypeAlias = List[int]


def main():
    strings_and_outputs_list = _read_data(data_file_path=os.path.join(os.path.dirname(__file__), "data.txt"))

    nums = []
    for strings, outputs in strings_and_outputs_list:
        codes = []
        for string in strings:
            codes.append([_letter_to_int(x) for x in string])

        output_codes = []
        for output_code in outputs:
            output_codes.append([_letter_to_int(x) for x in output_code])

        true_code_nums_by_apparent_code_num = _decode(codes=codes)
        output = 0
        for output_code in output_codes:
            output *= 10
            output += _num_by_string_nums([true_code_nums_by_apparent_code_num[x] for x in output_code])

        nums.append(output)

    print(sum(nums))


def _read_data(data_file_path: str) -> List[Tuple[List[str], List[str]]]:
    with open(data_file_path, "r") as file:
        lines = file.readlines()

    ret = []
    for line in lines:
        strings = [x.lstrip().rstrip() for x in re.split(" \\| | ", line.lstrip().rstrip())]
        ret.append((strings[:10], strings[10:]))

    return ret


def _letter_to_int(letter: str) -> int:
    return ord(letter) - 97


def _decode(codes: List[_Code]) -> Dict[int, int]:
    """Returns a mapping where the keys are the apparent code nums and the values are the true code nums.

    Based on the 10 codes representing 10 digits (0-9) (unordered), returns the mapping between strings to digits.
    """
    signatures = _get_unique_occurrence_tuples_and_num_total_occurrences(codes)

    true_code_nums_by_apparent_code_num = {}
    true_code_nums_by_apparent_code_num[signatures.index(((0, 0, 1, 1), 8))] = 0
    true_code_nums_by_apparent_code_num[signatures.index(((0, 1, 0, 1), 6))] = 1
    true_code_nums_by_apparent_code_num[signatures.index(((1, 1, 1, 1), 8))] = 2
    true_code_nums_by_apparent_code_num[signatures.index(((0, 1, 0, 1), 7))] = 3
    true_code_nums_by_apparent_code_num[signatures.index(((0, 0, 0, 1), 4))] = 4
    true_code_nums_by_apparent_code_num[signatures.index(((1, 1, 1, 1), 9))] = 5
    true_code_nums_by_apparent_code_num[signatures.index(((0, 0, 0, 1), 7))] = 6

    return true_code_nums_by_apparent_code_num


def _get_unique_occurrence_tuples_and_num_total_occurrences(codes: List[_Code]) -> List[Tuple[Tuple[int, ...], int]]:
    # The return is used as a signature (like a feature vector) to uniquely identify code nums.
    code_lengths = [len(x) for x in codes]
    one_four_seven_eight_codes = [codes[code_lengths.index(x)] for x in [2, 4, 3, 7]]
    ret = []
    for letter_index in range(7):
        unique_occurrences_tuple = tuple(int(letter_index in x) for x in one_four_seven_eight_codes)
        num_total_occurrences = sum([letter_index in x for x in codes])
        ret.append((unique_occurrences_tuple, num_total_occurrences))
    return ret


def _num_by_string_nums(string_nums: List[int]) -> int:
    on_off_status = ()
    for i in range(7):
        on_off_status += (int(i in string_nums),)
    return _num_by_on_off_status(on_off_status=on_off_status)


def _num_by_on_off_status(on_off_status: Tuple[int, ...]) -> int:
    return {
        (1, 1, 1, 0, 1, 1, 1): 0,
        (0, 0, 1, 0, 0, 1, 0): 1,
        (1, 0, 1, 1, 1, 0, 1): 2,
        (1, 0, 1, 1, 0, 1, 1): 3,
        (0, 1, 1, 1, 0, 1, 0): 4,
        (1, 1, 0, 1, 0, 1, 1): 5,
        (1, 1, 0, 1, 1, 1, 1): 6,
        (1, 0, 1, 0, 0, 1, 0): 7,
        (1, 1, 1, 1, 1, 1, 1): 8,
        (1, 1, 1, 1, 0, 1, 1): 9,
    }[on_off_status]


if __name__ == "__main__":
    main()
