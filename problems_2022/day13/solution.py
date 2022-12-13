"""https://adventofcode.com/2022/day/13."""
import os
from typing import Tuple, List, Any

import numpy as np

from adventofcode.util import read_lines_stripping_both_ends


class Packet:
    def __init__(self, value: List[Any]) -> None:
        self.value = value

    def __lt__(self, other: "Packet") -> bool:
        # If left is less than right, the order is correct (==1).
        # To be able to use Python's `sorted`, only `__lt__()` needs to be implemented.
        return self._is_right_order(left=self.value, right=other.value) == 1

    @staticmethod
    def _is_right_order(left, right):
        """Returns 1 if the order is right; -1 if the order is wrong; 0 if both are equal."""
        for left_item, right_item in zip(left, right):
            if isinstance(left_item, int) and isinstance(right_item, int):
                if left_item < right_item:
                    return 1

                if left_item > right_item:
                    return -1

                # Items are equal; continue to check the next value.
                continue

            # At least one of the items is a list.  Convert any int-typed item to a list as well.
            if isinstance(left_item, int):
                left_item = [left_item]

            if isinstance(right_item, int):
                right_item = [right_item]

            is_right_order = Packet._is_right_order(left=left_item, right=right_item)
            if is_right_order == 0:
                # Both items are equal. Continue to check the next.
                continue

            return is_right_order

        # All comparisons are equal. Check if any list has remaining elements.
        return int(np.sign(len(right) - len(left)))


def main():
    data = _read_data(data_file_path=os.path.join(os.path.dirname(__file__), "data.txt"))

    indices = []
    for idx, (left, right) in enumerate(data):
        if left < right:
            indices.append(idx + 1)

    print(f"Part 1: The sum of indices of right order is {sum(indices)}.")

    # Sort all packets along with the decoder packets.
    all_packets = []
    for packet_pair in data:
        all_packets.extend([packet_pair[0], packet_pair[1]])
    decoder_packets = [Packet(value=[[2]]), Packet(value=[[6]])]
    all_packets.extend(decoder_packets)
    sorted_packets = list(sorted(all_packets))

    # Find the decoder packet positions.
    decoder_packet_values = [x.value for x in decoder_packets]
    decoder_positions = []
    for packet_idx, packet in enumerate(sorted_packets):
        if packet.value in decoder_packet_values:
            decoder_positions.append(packet_idx + 1)
    print(f"Part 2: The product of decoder packet positions is {np.prod(decoder_positions).item()}.")


def _read_data(data_file_path: str) -> List[Tuple[Packet, Packet]]:
    """Returns the list of (left, right) tuples."""
    ret = []
    for line_idx, line in enumerate(read_lines_stripping_both_ends(file_path=data_file_path)):
        if line_idx % 3 == 0:
            left = eval(line)
        elif line_idx % 3 == 1:
            right = eval(line)
        else:
            ret.append((Packet(value=left), Packet(value=right)))

    # Need to append the last pair.
    ret.append((Packet(value=left), Packet(value=right)))

    return ret


if __name__ == "__main__":
    main()
