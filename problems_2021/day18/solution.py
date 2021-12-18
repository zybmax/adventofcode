"""https://adventofcode.com/2021/day/18."""
import itertools
import json
import os.path
from typing import List
from typing import Optional
from typing import Tuple

from binarytree import Node


def main():
    root_nodes = _read_data(data_file_path=os.path.join(os.path.dirname(__file__), "data.txt"))

    summed = root_nodes[0]
    for root in root_nodes[1:]:
        summed = _add(summed, root)

    print("Part 1: ", _calculate_magnitude(summed))

    max_sum_of_two = -float("inf")
    num_numbers = len(root_nodes)
    for i, j in itertools.product(range(num_numbers), range(num_numbers)):
        if i == j:
            continue

        root_nodes = _read_data(data_file_path=os.path.join(os.path.dirname(__file__), "data.txt"))
        current_sum = _calculate_magnitude(_add(root_nodes[i], root_nodes[j]))
        if current_sum > max_sum_of_two:
            max_sum_of_two = current_sum
    print("Part 2: ", max_sum_of_two)


def _read_data(data_file_path: str) -> List[Node]:
    """Returns a list of snailfish numbers as a list of root nodes for binary trees."""
    with open(data_file_path, "r") as file:
        lines = file.readlines()

    ret = []
    for line in lines:
        num_as_list = json.loads(line.lstrip().rstrip())
        root_node = Node(value=-1)
        _build_binary_tree(num_as_list, root_node)
        ret.append(root_node)

    return ret


def _build_binary_tree(tree_as_list: List, root_node: Node) -> None:
    """Builds a binary tree off of `root_node` from `tree_as_list`.

    For nodes that do not have a value but only have left and right children, use -1 as the value.
    """
    left, right = tree_as_list

    if isinstance(left, int):
        root_node.left = Node(value=left)
    else:
        root_node.left = Node(value=-1)
        _build_binary_tree(tree_as_list=left, root_node=root_node.left)

    if isinstance(right, int):
        root_node.right = Node(value=right)
    else:
        root_node.right = Node(value=-1)
        _build_binary_tree(tree_as_list=right, root_node=root_node.right)


def _inorder_traversal(node: Node, depth: int) -> List[Tuple[Node, int]]:
    """Appends a list of (node, depth) pairs to the input `nodes_and_depths`.

    The real root node has depth of 0.
    """
    if node.value != -1:
        return [(node, depth)]

    return _inorder_traversal(node.left, depth + 1) + [(node, depth)] + _inorder_traversal(node.right, depth + 1)


def _add(first_root: Node, second_root: Node) -> Node:
    new_root = Node(-1, left=first_root, right=second_root)

    # Traverse all the nodes while giving out the depth (root has depth of 0) of each node. Then for the nodes at depth
    # of 4, check whether it has children that have left and right children. If so, execute the explosion rule. If there
    # is no node to explode, check the splitting rule for nodes that have value larger than 10, and execute the
    # splitting rule. Because we always need to check the leftmost node, we should do inorder traversal.
    while True:
        nodes_and_depths = _inorder_traversal(new_root, depth=0)
        node_index = _parent_node_index_for_explosion(nodes_and_depths)
        if node_index is not None:
            _execute_explosion(inorder_nodes=[x[0] for x in nodes_and_depths], parent_node_index=node_index)
            continue

        node_for_splitting = _node_for_splitting(nodes_and_depths)
        if node_for_splitting is None:
            break

        node_for_splitting.left = Node(node_for_splitting.value // 2)
        node_for_splitting.right = Node(node_for_splitting.value - node_for_splitting.value // 2)
        node_for_splitting.value = -1

    return new_root


def _parent_node_index_for_explosion(nodes_and_depths: List[Tuple[Node, int]]) -> Optional[int]:
    """Returns the index of the node in `nodes_and_depths` that should undergo explosion.

    Returns None if it does not exist.
    """
    for i, (node, depth) in enumerate(nodes_and_depths):
        if depth == 4 and node.value == -1:
            return i

    return None


def _execute_explosion(inorder_nodes: List[Node], parent_node_index: int) -> None:
    node_to_explode = inorder_nodes[parent_node_index]

    for i in range(parent_node_index - 2, -1, -1):
        if inorder_nodes[i].value != -1:
            inorder_nodes[i].value += node_to_explode.left.value
            break

    for i in range(parent_node_index + 2, len(inorder_nodes)):
        if inorder_nodes[i].value != -1:
            inorder_nodes[i].value += node_to_explode.right.value
            break

    node_to_explode.value = 0
    node_to_explode.left = None
    node_to_explode.right = None


def _node_for_splitting(nodes_and_depths: List[Tuple[Node, int]]) -> Optional[Node]:
    for node, depth in nodes_and_depths:
        if node.value >= 10:
            return node

    return None


def _calculate_magnitude(root: Node) -> int:
    if root.value != -1:
        return root.value

    return 3 * _calculate_magnitude(root.left) + 2 * _calculate_magnitude(root.right)


if __name__ == "__main__":
    main()
