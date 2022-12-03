"""https://adventofcode.com/2021/day/15.

Use Dijkstra's algorithm for finding the shortest path with weights.
"""
import itertools
import os.path
from typing import Tuple

import networkx as nx
import numpy as np

_Point = Tuple[int, int]


def main():
    risk_level_map = _expand_array_5x(_read_data(data_file_path=os.path.join(os.path.dirname(__file__), "data.txt")))

    graph = _graph_from_2d_array(risk_level_map)
    path = nx.dijkstra_path(graph, source=(0, 0), target=(risk_level_map.shape[0] - 1, risk_level_map.shape[1] - 1))
    print(sum(risk_level_map[i, j] for i, j in path[1:]))


def _read_data(data_file_path: str) -> np.ndarray:
    """Returns the risk level map."""
    with open(data_file_path, "r") as file:
        lines = file.readlines()

    return np.array([[int(x) for x in line.lstrip().rstrip()] for line in lines], dtype=np.uint8)


def _expand_array_5x(array: np.ndarray) -> np.ndarray:
    ret = np.zeros(shape=(array.shape[0] * 5, array.shape[1] * 5), dtype=np.uint8)
    for i, j in itertools.product(range(5), range(5)):
        ret[i * array.shape[0] : (i + 1) * array.shape[0], j * array.shape[1] : (j + 1) * array.shape[1],] = (
            array + i + j
        )
    ret = np.mod(ret - 1, 9) + 1
    return ret


def _graph_from_2d_array(array: np.ndarray) -> nx.DiGraph:
    """Returns a directed graph from a 2D array.

    Each pixel is a node, and is connected to its 4 neighbors (diagonal neighbors are not connected) with bidirectional
    edges. The weight of each edge is equal to the value of the array element that it ends in.
    """
    graph = nx.DiGraph()
    height, width = array.shape

    # Add all pixels as nodes.
    graph.add_nodes_from((i, j) for i, j in itertools.product(range(height), range(width)))

    # Add edges. Start from upper-left and only add the edges to and from the nodes to the right and below the current
    # node.
    for i, j, is_forward, axis in itertools.product(range(height), range(width), [True, False], [0, 1]):
        start_node = (i, j)
        end_node = (i + 1, j) if axis == 0 else (i, j + 1)

        if end_node[0] > height - 1 or end_node[1] > width - 1:
            # Out of bottom or right bounds.
            continue

        if not is_forward:
            start_node, end_node = end_node, start_node

        graph.add_edge(start_node, end_node, weight=array[end_node[0], end_node[1]])

    return graph


if __name__ == "__main__":
    main()
