"""https://adventofcode.com/2022/day/7."""
import os
from typing import List, Optional
from dataclasses import dataclass

from adventofcode.util import read_lines_stripping_both_ends


@dataclass
class Node:
    """A node representing a directory or a file.

    Args:
        name: The name of the current directory or file.
        size: The size of the directory or file.
        parent: The parent node.  If root, parent is None.
        subdirectories: A list of subdirectories.  Defaults to None to indicate it is a file.
        files: A list of files in the directory.  Defaults to None to indicate it is a file.
    """

    name: str
    size: int
    parent: Optional["Node"]
    subdirectories: Optional[List["Node"]] = None
    files: Optional[List["Node"]] = None

    def is_file(self) -> bool:
        return self.subdirectories is None


def main():
    lines = _read_data(data_file_path=os.path.join(os.path.dirname(__file__), "data.txt"))
    root = construct_tree(inputs=lines)

    sizes = []
    list_directory_sizes(root=root, sizes=sizes)
    print(
        f"Part 1: The total size of directories with sizes under 100000 is "
        f"{sum(size for size in sizes if size <= 100000)}."
    )

    total_size = root.size
    min_freed_space = 30000000 - (70000000 - total_size)
    print(
        f"Part 2: The smallest folder to delete, which will free up enough space, has size of "
        f"{min(x for x in sizes if x >= min_freed_space)}."
    )


def _read_data(data_file_path: str) -> List[str]:
    return read_lines_stripping_both_ends(file_path=data_file_path)


def construct_tree(inputs: List[str]) -> Node:
    """Returns the root node of a file system tree."""
    root = _construct_tree_without_computing_directory_sizes(inputs=inputs)
    _compute_directory_sizes(root=root)
    return root


def _construct_tree_without_computing_directory_sizes(inputs: List[str]) -> Node:
    root = Node(name="/", size=0, parent=None, subdirectories=[], files=[])
    current_node = root

    # Make all folders have size of 0 temporarily.
    for line in inputs:
        if line.startswith("$ cd"):
            # A command to move to a specific directory.
            argument = line[5:]

            if argument == "/":
                current_node = root
                continue

            if argument == "..":
                # Move to the previous directory.
                current_node = current_node.parent
                continue

            # It is a "cd some_subdirectory" command.
            index = [x.name for x in current_node.subdirectories].index(argument)
            current_node = current_node.subdirectories[index]
            continue

        if line.startswith("$ ls"):
            # The following lines will be directories or filenames with sizes.  Nothing to do.
            continue

        # The current line is an output of the "ls" command.
        if line.startswith("dir"):
            directory_name = line[4:]
            if directory_name in [x.name for x in current_node.subdirectories]:
                # This subdirectory is already known.  Do nothing.
                continue

            # New subdirectory.  Add it to the tree.
            new_child = Node(name=directory_name, size=0, parent=current_node, subdirectories=[], files=[])
            current_node.subdirectories.append(new_child)
            continue

        # The line starts with the size and file name.
        size, filename = line.split(" ")
        size = int(size)
        new_file = Node(name=filename, size=size, parent=current_node)
        current_node.files.append(new_file)

    return root


def _compute_directory_sizes(root: Node) -> None:
    """Update all directory sizes of the current tree."""
    if root.is_file():
        # The file size is already there.  Do nothing.
        return

    for subdirectory in root.subdirectories:
        _compute_directory_sizes(root=subdirectory)

    root.size = sum(x.size for x in (root.files + root.subdirectories))


def list_directory_sizes(root: Node, sizes: List[int]) -> None:
    """Traverses the tree and appends all directories' sizes to the `sizes` list."""
    if root.is_file():
        return

    sizes.append(root.size)

    for dir_ in root.subdirectories:
        list_directory_sizes(root=dir_, sizes=sizes)


if __name__ == "__main__":
    main()
