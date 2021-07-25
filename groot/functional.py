"""functions used by tree class."""
from typing import Dict, List, Optional, Set, Tuple, Union

from .node import Node


def build_nodes(child_to_parent: Dict[str, str]) -> Dict[str, Node]:
    """
    Build dictionary of nodes from child-to-parent mapping.

    Parameters
    ----------
    child_to_parent : Dict[str, str]
        Maps child node name to its parent's name.

    Returns
    -------
    Dict[str, Node]
        Lookup table for all nodes: name -> Node where Node contains
        - parent name
        - set of child names
    """

    nodes: Dict[str, Node] = dict()

    def init(name):
        nodes[name] = Node(name, child_to_parent[name])

    for c, p in child_to_parent.items():

        if not p:  # if root skip
            continue

        if p not in nodes:
            init(p)

        nodes[p].children.add(c)

        if c not in nodes:
            init(c)

    return nodes


def push_atoms(
    nodes: Dict[str, Node],
    atoms: Optional[Union[Set[str], List[str], Tuple[str]]] = None,
) -> None:
    """
    Push atoms to all nodes.

    Parameters
    ----------
    nodes : Dict[str, Node]
        Lookup table of `nodes`.
    atoms : Optional[Union[Set[str], List[str], Tuple[str]]]
        Given set of `atoms`. If None, `atoms` will be inferred from `nodes`
    """

    def _get_atoms(node: Node) -> Set[str]:

        if node.atoms:
            return node.atoms

        if node.is_atom:
            node.atoms.add(node.name)
            return node.atoms

        for c in node.children:
            node.atoms.update(_get_atoms(nodes[c]))

        return node.atoms

    if atoms is None:
        atoms = [k for k, v in nodes.items() if v.is_atom]
    else:
        atoms = list(atoms)

    atoms.sort()

    for name, node in nodes.items():

        if node.atoms:
            continue

        _ = _get_atoms(node)


def all_leaf_nodes(root: str, nodes: Dict[str, Node]) -> Set[str]:
    """
    Get all leaf nodes of a given root (included).

    Parameters
    ----------
    root : str
        Name of `root` which should be in nodes.
    nodes : Dict[str, Node]
        Lookup table of `nodes`.

    Returns
    -------
    Set[str]
        Set of all leaf nodes including root.
    """

    root_node = nodes[root]
    leaf_nodes = {root}
    if root_node.is_atom:
        return leaf_nodes
    for c in root_node.children:
        leaf_nodes.update(all_leaf_nodes(c, nodes))

    return leaf_nodes


def index_nodes_by_level(
    nodes: Dict[str, Node]
) -> Tuple[Dict[str, int], List[Set[str]]]:
    """
    Assign levels to given nodes.

    Parameters
    ----------
    nodes : Dict[str, Node]
        Lookup table of nodes.

    Returns
    -------
    Tuple[Dict[str, int], List[Set[str]]]
        Level lookup table, and levels of nodes.
    """

    node_level = {name: None for name in nodes}

    def _get_level(node: Node) -> int:

        if node_level[node.name] is not None:
            return node_level[node.name]

        if node.is_root:
            node_level[node.name] = 0
            return 0

        node_level[node.name] = _get_level(nodes[node.parent]) + 1

        return node_level[node.name]

    for node in nodes.values():
        _ = _get_level(node)

    levels = {}

    for k, v in node_level.items():
        if v in levels:
            levels[v].add(k)
        else:
            levels[v] = {k}

    levels = [levels[l] for l in range(len(levels))]

    return node_level, levels
