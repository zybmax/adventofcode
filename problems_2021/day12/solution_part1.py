"""https://adventofcode.com/2021/day/12.

Represent a graph using a dict where the nodes are keys, and each value is the connected nodes of that node.
"""
import os.path
from typing import Dict
from typing import List
from typing import Set


# Type alias for a graph: a mapping between nodes and the connected nodes.
_Graph = Dict[str, Set[str]]


def main():
    graph = _read_data(
        data_file_path=os.path.join(os.path.dirname(__file__), "data.txt")
    )

    print(_GraphPathFinder(graph=graph).num_paths)


def _read_data(data_file_path: str) -> _Graph:
    with open(data_file_path, "r") as file:
        lines = file.readlines()

    ret = {}
    for line in lines:
        start_node, end_node = line.lstrip().rstrip().split("-")

        # Undirected graph, so the connections are two-directional.
        if start_node in ret:
            ret[start_node].add(end_node)
        else:
            ret[start_node] = {end_node}

        if end_node in ret:
            ret[end_node].add(start_node)
        else:
            ret[end_node] = {start_node}

    return ret


class _GraphPathFinder:
    def __init__(self, graph: _Graph) -> None:
        self._graph = graph
        self._num_paths = 0

        self._find_path_recursive(["start"])

    def _find_path_recursive(self, path: List[str]) -> None:
        if path[-1] == "end":
            self._num_paths += 1
            return

        for neighbor in self._graph[path[-1]]:
            if neighbor == neighbor.lower() and neighbor in path:
                continue

            self._find_path_recursive(path + [neighbor])

    @property
    def num_paths(self) -> int:
        return self._num_paths


if __name__ == "__main__":
    main()
