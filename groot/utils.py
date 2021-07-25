"""Provide additional utils for tree class."""
from .tree import Node, Tree

__all__ = ["draw_tree"]


def draw_tree(
    tree: Tree, tree_space: int = 3, atom_marker: str = "■", show_level: bool = True
) -> str:
    """
    Plot tree structure.

    Parameters
    ----------
    tree : Tree
        A `Tree` object.
    tree_space : int
        Number of space in markers.
    atom_marker : str
        Marker for atom nodes.
    show_level : bool
        If `True` levels will be added as a header

    Returns
    -------
    str
        Tree diagram string.

    Example
    -------
    ```
    draw_tree(tree, show_level=True)

    0   1   2
    ┼───┼───┼
    a
    ├── a.a
    │   ├── a.a.b ■
    │   └── a.a.a ■
    ├── a.c ■
    └── a.b
        └── a.b.a ■
    b
    ├── b.a ■
    └── b.b ■
    ```
    """

    tree_space = max(int(tree_space), 1)

    class Marker:
        SPACE = " " * (tree_space + 1)
        BRANCH = "│" + " " * tree_space
        TEE = "├" + "─" * (tree_space - 1) + " "
        LAST = "└" + "─" * (tree_space - 1) + " "

    def draw(node: Node, prefix: str = ""):
        """Based on stackoverflow: `List directory tree structure in python`."""

        children = node.children
        # contents each get pointers that are ├── with a final └── :
        markers = [Marker.TEE] * (len(children) - 1) + [Marker.LAST]
        for marker, child in zip(markers, children):

            if nodes[child].is_atom:
                yield prefix + marker + child + " " + atom_marker
            else:
                yield prefix + marker + child
                extension = Marker.BRANCH if marker == Marker.TEE else Marker.SPACE
                yield from draw(nodes[child], prefix=prefix + extension)

    nodes = tree.nodes

    lines = []
    if show_level:
        gap = " " * tree_space
        lines.append(
            gap.join("\b" * (len(str(l)) - 1) + str(l) for l in range(len(tree.levels)))
        )
        dash = "─" * tree_space
        lines.append(dash.join("┼" for l in range(len(tree.levels))))

    for root in tree.roots:
        lines.append(root)
        for ln in draw(nodes[root]):
            lines.append(ln)

    return "\n".join(lines)
