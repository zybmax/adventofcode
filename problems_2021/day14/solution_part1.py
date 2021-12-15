"""https://adventofcode.com/2021/day/14."""
import os.path
from collections import Counter
from typing import Dict
from typing import List
from typing import Tuple

# The insertion rule is a mapping where each key is the (left_char, right_char), and each value is the char to insert
# between them.
_InsertionRule = Dict[Tuple[str, str], str]


def main():
    template, insertion_rule = _read_data(data_file_path=os.path.join(os.path.dirname(__file__), "data.txt"))

    template_as_list = [x for x in template]
    for i in range(10):
        _do_one_step_insertion(template_as_list=template_as_list, insertion_rule=insertion_rule)

    print("".join(template_as_list))

    counter = Counter(template_as_list)
    # `most_common` returns a list of the (element, count) tuples.
    most_common = counter.most_common()
    print(most_common[0][1] - most_common[-1][1])


def _read_data(data_file_path: str) -> Tuple[str, _InsertionRule]:
    """Returns the template and the pair insertion rules.
    """
    with open(data_file_path, "r") as file:
        lines = file.readlines()

    insertion_rules = {}

    for line in lines[2:]:
        char_pair, char_to_insert = line.lstrip().rstrip().split(" -> ")
        insertion_rules[(char_pair[0], char_pair[1])] = char_to_insert

    return lines[0].lstrip().rstrip(), insertion_rules


def _do_one_step_insertion(template_as_list: List[str], insertion_rule: _InsertionRule) -> None:
    """Modifies `template_as_list` in-place to do one-step pair insertion."""
    num_chars = len(template_as_list)
    # The offset caused by inserting new characters.
    offset = 0
    for i in range(num_chars - 1):
        try:
            template_as_list.insert(
                i + offset + 1, insertion_rule[(template_as_list[i + offset], template_as_list[i + offset + 1],)],
            )
        except KeyError:
            continue

        offset += 1


if __name__ == "__main__":
    main()
