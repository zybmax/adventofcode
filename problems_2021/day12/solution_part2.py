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
    graph = _read_data(data_file_path=os.path.join(os.path.dirname(__file__), "data.txt"))

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

        self._find_path_recursive(path=["start"], small_cave_visited_twice=False)

    def _find_path_recursive(self, path: List[str], small_cave_visited_twice: bool) -> None:
        if path[-1] == "end":
            self._num_paths += 1
            return

        for neighbor in self._graph[path[-1]]:
            if neighbor.isupper() or neighbor not in path:
                self._find_path_recursive(path + [neighbor], small_cave_visited_twice=small_cave_visited_twice)
                continue

            # Neighbor already in path. If there is already a small cave visited twice, then this path will not work.
            # If there is no small cave visited twice, then we can choose this neighbor to visit twice; if we don't
            # choose to visit this cave twice, then this path also does not work.
            # "Start" node can only be visited once.
            if neighbor == "start" or small_cave_visited_twice:
                continue

            self._find_path_recursive(path + [neighbor], small_cave_visited_twice=True)

    @property
    def num_paths(self) -> int:
        return self._num_paths


if __name__ == "__main__":
    main()
