"""https://adventofcode.com/2022/day/12."""
import itertools
import os
from typing import Tuple

import networkx as nx
import numpy as np

from adventofcode.util import read_lines_stripping_both_ends


def main():
    height_map, start_position, end_position = _read_data(
        data_file_path=os.path.join(os.path.dirname(__file__), "data.txt")
    )
    graph = _build_graph(height_map=height_map)
    shortest_path_length = nx.shortest_path_length(G=graph, source=start_position, target=end_position)
    print(f"Part 1: The shortest path length is {shortest_path_length}.")

    min_trail_length = float("inf")
    for node_idx, path_length in nx.single_target_shortest_path_length(G=graph, target=end_position):
        if height_map[node_idx[0], node_idx[1]] != 0:
            continue

        min_trail_length = min(min_trail_length, path_length)
    print(f"Part 2: The shortest trail length is {min_trail_length}.")


def _read_data(data_file_path: str) -> Tuple[np.ndarray, Tuple[int, int], Tuple[int, int]]:
    """Returns the (height map, start position, end position)."""
    ret = []
    start_position = None
    end_position = None
    for line_idx, line in enumerate(read_lines_stripping_both_ends(file_path=data_file_path)):
        row = []
        for column_idx, char in enumerate(line):
            if char == "S":
                # Start point has height of "a", i.e., 0.
                row.append(0)
                start_position = (line_idx, column_idx)
                continue

            if char == "E":
                # End point has height of "z", i.e., 25.
                row.append(25)
                end_position = (line_idx, column_idx)
                continue

            # The ASCII index of "a" is 97.
            row.append(ord(char) - 97)

        ret.append(row)

    return np.array(ret, dtype=int), start_position, end_position


def _build_graph(height_map: np.ndarray) -> nx.DiGraph:
    # For each (y, x) point, add an edge to the neighbors if the destination_height <= source_height + 1.
    ret = nx.DiGraph()
    indices = list(itertools.product(range(height_map.shape[0]), range(height_map.shape[1])))
    for idx_y, idx_x in indices:
        ret.add_node(node_for_adding=(idx_y, idx_x))

    for idx_y, idx_x in indices:
        # Only check the neighbors in the right and down directions to avoid duplication.
        for neighbor in [(idx_y - 1, idx_x), (idx_y + 1, idx_x), (idx_y, idx_x - 1), (idx_y, idx_x + 1)]:
            if (
                0 <= neighbor[0] <= height_map.shape[0] - 1
                and 0 <= neighbor[1] <= height_map.shape[1] - 1
                and height_map[neighbor[0], neighbor[1]] - height_map[idx_y, idx_x] <= 1
            ):
                ret.add_edge(u_of_edge=(idx_y, idx_x), v_of_edge=neighbor)

    return ret


if __name__ == "__main__":
    main()
