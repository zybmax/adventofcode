"""https://adventofcode.com/2021/day/14.

The assumption made is that the insertion rule contains all possible char pairs (N x N, for N unique chars) in the
chars being considered. The problem input satisfies that assumption.
"""
import os.path
from collections import Counter
from typing import Counter as _CounterType
from typing import Dict
from typing import Tuple

# The insertion rule is a mapping where each key is the (left_char, right_char), and each value is the char to insert
# between them.
_InsertionRule = Dict[Tuple[str, str], str]


def main():
    template, insertion_rule = _read_data(
        data_file_path=os.path.join(os.path.dirname(__file__), "data.txt")
    )

    # Find all valid chars.
    all_chars = set()
    for pair in insertion_rule:
        all_chars.add(pair[0])
        all_chars.add(pair[1])
    if len(insertion_rule) != len(all_chars) ** 2:
        raise RuntimeError(
            "The number of insertion rules must be equal to the number of unique chars squared!"
        )

    # Find the counts of all char pairs in the original template.
    all_char_pair_counts = Counter()
    for i in range(len(template) - 1):
        all_char_pair_counts[(template[i], template[i + 1])] += 1

    for i in range(40):
        all_char_pair_counts = _do_one_step_insertion(
            all_char_pair_counts, insertion_rule
        )

    char_count = Counter()
    for (left_char, right_char), count in all_char_pair_counts.items():
        char_count[left_char] += count
        char_count[right_char] += count

    # Except for the start char and end char, every char is counted twice.
    char_count[template[0]] += 1
    char_count[template[-1]] += 1
    char_count = Counter({x: y // 2 for x, y in char_count.items()})

    most_common = char_count.most_common()
    print(most_common[0][1] - most_common[-1][1])


def _read_data(data_file_path: str) -> Tuple[str, _InsertionRule]:
    """Returns the template and the pair insertion rules."""
    with open(data_file_path, "r") as file:
        lines = file.readlines()

    insertion_rules = {}

    for line in lines[2:]:
        char_pair, char_to_insert = line.lstrip().rstrip().split(" -> ")
        insertion_rules[(char_pair[0], char_pair[1])] = char_to_insert

    return lines[0].lstrip().rstrip(), insertion_rules


def _do_one_step_insertion(
    all_char_pair_counts: _CounterType, insertion_rule: _InsertionRule
) -> _CounterType:
    """Returns a new counter with keys being the char pairs and values being the counts after one step insertion."""
    ret = Counter()

    for key, count in all_char_pair_counts.items():
        ret[(key[0], insertion_rule[key])] += count
        ret[(insertion_rule[key], key[1])] += count

    return ret


if __name__ == "__main__":
    main()
