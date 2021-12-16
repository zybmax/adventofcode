"""https://adventofcode.com/2021/day/16."""
import functools
import operator
import os.path
from typing import List
from typing import Tuple
from typing import Union


# Every packet is made up of a version, a type ID, followed by a single number (literal) or a list of sub-packets.
# A literal packet is a leaf of the tree, whereas an operator packet is always a container of multiple other packets.
_Packet = Tuple[int, int, Union[int, List]]

_LITERAL_TYPE_ID = 4


def main():
    message = _read_data(data_file_path=os.path.join(os.path.dirname(__file__), "data.txt"))

    packets = _decode(message)

    print(f"Part 1: Sum of all versions is {_sum_versions(packets)}")
    print(f"Part 2: Evaluated expression is {_evaluate_expression(packets[0])}")


def _read_data(data_file_path: str) -> str:
    """Returns the risk level map."""
    with open(data_file_path, "r") as file:
        return file.readline().lstrip().rstrip()


def _decode(hex_message: str) -> List[_Packet]:
    """Returns a list of decoded packets from the hex message input."""
    # Convert hex message to binary while keeping the leading zeros.
    # After converting to binary, remove the first two chars "0b". Fill zeros on the left to attain the desired total
    # length.
    binary_message = bin(int(hex_message, 16))[2:].zfill(len(hex_message) * 4)

    ret = []
    position = 0
    # The remaining bits must at least be longer than 6 that make up a header.
    while len(hex_message) - position > 6:
        packet, position = _decode_packet(binary_message, position)
        ret.append(packet)

    return ret


def _decode_packet(binary_message, position) -> Tuple[_Packet, int]:
    """Returns a decoded packet and the position after decoding the current packet.

    The input position is before the header bits for the current packet.
    """
    version = int(binary_message[position : position + 3], 2)
    type_id = int(binary_message[position + 3 : position + 6], 2)
    position += 6

    if type_id == _LITERAL_TYPE_ID:
        num, position = _decode_literal_content(binary_message, position_after_header=position)
        return (version, type_id, num), position

    # This is an operator and needs to be decoded recursively.
    length_type = binary_message[position]
    position += 1

    sub_packets = []
    if length_type == "0":
        total_num_bits = int(binary_message[position : position + 15], 2)
        position += 15

        end_position = position + total_num_bits
        while position < end_position:
            sub_packet, position = _decode_packet(binary_message, position)
            sub_packets.append(sub_packet)

        return (version, type_id, sub_packets), position

    # Length type is 1.
    num_sub_packets = int(binary_message[position : position + 11], 2)
    position += 11
    for i in range(num_sub_packets):
        sub_packet, position = _decode_packet(binary_message, position)
        sub_packets.append(sub_packet)
    return (version, type_id, sub_packets), position


def _decode_literal_content(binary_message, position_after_header) -> Tuple[int, int]:
    """Returns a single number parsed from the packet and the new position.

    The input position is the first position after the header for the current packet.
    """
    binary_num = ""
    while True:
        binary_num = binary_num + binary_message[position_after_header + 1 : position_after_header + 5]
        position_after_header += 5

        # If the last leading binary is 0, stop.
        if binary_message[position_after_header - 5] == "0":
            break

    return int(binary_num, 2), position_after_header


def _sum_versions(packets: List[_Packet]) -> int:
    total = 0
    for packet in packets:
        total += packet[0]

        if packet[1] != _LITERAL_TYPE_ID:
            total += _sum_versions(packet[2])

    return total


def _evaluate_expression(packet: _Packet) -> int:
    """Returns the evaluated expression for a packet."""
    type_id = packet[1]
    if type_id == _LITERAL_TYPE_ID:
        return packet[2]

    # Operator packet.
    sub_packets = packet[2]
    sub_packet_expressions = [_evaluate_expression(x) for x in sub_packets]
    if type_id == 0:
        return sum(sub_packet_expressions)

    if type_id == 1:
        return functools.reduce(operator.mul, sub_packet_expressions, 1)

    if type_id == 2:
        return min(sub_packet_expressions)

    if type_id == 3:
        return max(sub_packet_expressions)

    if type_id == 5:
        return sub_packet_expressions[0] > sub_packet_expressions[1]

    if type_id == 6:
        return sub_packet_expressions[0] < sub_packet_expressions[1]

    if type_id == 7:
        return sub_packet_expressions[0] == sub_packet_expressions[1]


if __name__ == "__main__":
    main()
