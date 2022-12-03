"""https://adventofcode.com/2021/day/19.

For each pair of scanners, check if they can be registered (have 12 pairs of common beasons).  Build a bidirectional
graph to record this by adding edges (with the transformation matrix, and inverse transformation matrix) both ways.
After the graph is built, start from scanner 0, traverse all the nodes, and calculate the global transformation matrix
of each scanner w.r.t. a common scanner (scanner 0), so we can finally compute the final set of points.
"""
import functools
import itertools
import os.path
from typing import List
from typing import Optional
from typing import Set
from typing import Tuple

import networkx as nx
import numpy as np

# 3D point in x, y, z.
_3DPoint = Tuple[int, int, int]

# The 0th element is the original axis number (0, 1 or 2), and the 1st element is the sign (1 or -1).
_RotatedAxis = Tuple[int, int]
# A rotation is represented by a length-three tuple of rotated axes, in the order of the new x, y and z axes.
_Rotation = Tuple[_RotatedAxis, _RotatedAxis, _RotatedAxis]

_SCANNER_RADIUS: int = 1000
_MIN_NUM_COMMON_BEACONS: int = 12


def main():
    point_sets = _read_data(data_file_path=os.path.join(os.path.dirname(__file__), "data.txt"))

    num_scanners = len(point_sets)
    # A directed graph whose edges store the transformation matrix between scanner pairs (as attribute
    # "local_transformation") and whose nodes store the transformation matrix between each scanner and scanner 0 (as
    # attribute "global_transformation").
    graph = nx.DiGraph()
    # Add all scanners as nodes.
    for i in range(num_scanners):
        graph.add_node(i)

    for first_scanner_index, second_scanner_index in itertools.combinations(range(num_scanners), 2):
        if nx.has_path(graph, first_scanner_index, second_scanner_index):
            continue

        transformation_matrix = _find_pairwise_transformation_matrix(
            point_sets[first_scanner_index], point_sets[second_scanner_index]
        )
        if transformation_matrix is not None:
            graph.add_edge(first_scanner_index, second_scanner_index, local_transformation=transformation_matrix)
            graph.add_edge(
                second_scanner_index, first_scanner_index, local_transformation=np.linalg.inv(transformation_matrix)
            )

    transformation_matrices: List[np.ndarray] = _find_global_transformation_matrices(graph)
    all_beacons = _gather_points(point_sets, transformation_matrices)

    print("Part 1: ", len(all_beacons))

    max_distance = max(
        int(
            np.sum(
                np.abs(
                    transformation_matrices[first_scanner_index][:3, 3]
                    - transformation_matrices[second_scanner_index][:3, 3]
                )
            )
        )
        for first_scanner_index, second_scanner_index in itertools.combinations(range(num_scanners), 2)
    )
    print("Part 2: ", max_distance)


def _read_data(data_file_path: str) -> List[Set[_3DPoint]]:
    """Returns a list 3D point lists, each representing the points detected by a single scanner."""
    with open(data_file_path, "r") as file:
        lines = file.readlines()

    ret = []
    for i, line in enumerate(lines):
        line = line.lstrip().rstrip()
        if line.startswith("---"):
            current_point_list = set()
            continue

        if not line:
            ret.append(current_point_list)
            continue

        current_point_list.add(tuple(int(x) for x in line.split(",")))

    # After the last point is scanned, append the last scanner's point list to the return.
    ret.append(current_point_list)
    return ret


def _find_pairwise_transformation_matrix(
    first_point_set: Set[_3DPoint], second_point_set: Set[_3DPoint]
) -> Optional[np.ndarray]:
    """Returns the 4x4 transformation matrix to transform the common points in the second point set into the first.

    (x, y, z, 1)^T = transformation @ (x', y', z', 1)^T where "prime" represents coordinates in the second set. The
    upper-left 3x3 submatrix only has three nonzero elements of -1 or 1, representing a rotation. The rightmost column
    is (x_shift, y_shift, z_shift, 1)^T. The bottom row is (0, 0, 0, 1).
    """
    for rotation in _all_rotations():
        rotated_second_point_set = set(_unrotate(x, rotation) for x in second_point_set)
        for first_point, second_point in itertools.product(first_point_set, rotated_second_point_set):
            shift = tuple(first_point[i] - second_point[i] for i in range(3))
            # Efficiency improvement. If a shift will result in the two scanners having no overlap, skip.
            if max(abs(x) for x in shift) > _SCANNER_RADIUS * 2:
                continue

            transformed_second_point_set = set(
                tuple(point[i] + shift[i] for i in range(3)) for point in rotated_second_point_set
            )
            if len(first_point_set.intersection(transformed_second_point_set)) >= _MIN_NUM_COMMON_BEACONS:
                return _transformation_matrix_from_rotation_and_shift(rotation, shift)

    return None


@functools.lru_cache(maxsize=1)
def _all_rotations() -> Set[_Rotation]:
    """Returns all possible valid rotations."""
    ret = set()
    for axes in itertools.permutations(range(3), 3):
        for signs in itertools.product([-1, 1], [-1, 1], [-1, 1]):
            rotation = tuple((axes[i], signs[i]) for i in range(3))
            if _is_right_hand_system(rotation):
                ret.add(tuple((axes[i], signs[i]) for i in range(3)))
    return ret


def _is_right_hand_system(rotation: _Rotation) -> bool:
    unit_vectors = []
    for i in range(3):
        unit_vector = np.zeros((3,), dtype=int)
        unit_vector[rotation[i][0]] = rotation[i][1]
        unit_vectors.append(unit_vector)

    return np.all(np.cross(unit_vectors[0], unit_vectors[1]) == unit_vectors[2])


def _unrotate(point: _3DPoint, rotation: _Rotation) -> _3DPoint:
    axes = tuple(x[0] for x in rotation)
    ret = ()
    for i in range(3):
        axis = axes.index(i)
        sign = rotation[axis][1]
        ret += (point[axis] * sign,)
    return ret


def _transformation_matrix_from_rotation_and_shift(rotation: _Rotation, shift: _3DPoint) -> np.ndarray:
    """Returns the 4x4 transformation matrix from rotation and shift.

    coordinate_in_original_system = transformation_matrix @ coordinate_in_transformed_system.
    """
    ret = np.zeros((4, 4), dtype=float)
    for i in range(3):
        ret[i, rotation[i][0]] = rotation[i][1]
    ret[:3, :3] = np.linalg.inv(ret[:3, :3])

    ret[3, 3] = 1

    for i in range(3):
        ret[i, 3] = shift[i]
    return ret


def _find_global_transformation_matrices(graph: nx.DiGraph) -> List[np.ndarray]:
    """Returns a list of transformation matrices of each scanner w.r.t. the 0th scanner."""
    nx.set_node_attributes(graph, {0: np.eye(4)}, "global_transformation")
    for next_node, previous_node in nx.dfs_predecessors(graph, 0).items():
        nx.set_node_attributes(
            graph,
            {
                next_node: graph.nodes[previous_node]["global_transformation"]
                @ graph.edges[(previous_node, next_node)]["local_transformation"]
            },
            "global_transformation",
        )

    return [graph.nodes[i]["global_transformation"] for i in range(graph.number_of_nodes())]


def _gather_points(point_sets, transformation_matrices) -> Set[_3DPoint]:
    """Returns the set of all beacons from the point sets detected by each scanner and their transformation matrices."""
    ret = set()
    for point_set, transformation_matrix in zip(point_sets, transformation_matrices):
        for point in point_set:
            ret.add(
                tuple(int(x) for x in (transformation_matrix @ np.array(point + (1,))[:, np.newaxis]).flatten())[:-1]
            )

    return ret


if __name__ == "__main__":
    main()
