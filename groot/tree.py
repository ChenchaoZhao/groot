"""Core data structures."""
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Dict, Optional, Set

import yaml

from .functional import all_leaf_nodes, build_nodes, index_nodes_by_level, push_atoms

__all__ = ["Node", "Tree"]


@dataclass
class Node:
    """
    Node data structure.

    Parameters
    ----------
    name : str
    parent: Optional[str]
    children: Set[str], initialized as set()
    atoms: Set[str], initialized as set()
    """

    name: str
    parent: Optional[str] = None
    children: Set[str] = field(default_factory=set)
    atoms: Set[str] = field(default_factory=set)

    @property
    def is_root(self) -> bool:
        """
        Check if the node is root node.

        Returns
        -------
        bool
            Node is root.
        """
        return self.parent is None

    @property
    def is_atom(self) -> bool:
        """
        Check if the node is atomic, i.e. the finest level.

        Returns
        -------
        bool
            Node is atomic.
        """
        return self.children == set()

    def __str__(self) -> str:
        """
        Display the parent-child relations of the node.

        Returns
        -------
        str
            Node relations.
        """
        if self.is_root:
            return f"*{self.name} -> {self.children}"
        else:
            return f"{self.parent} -> {self.name} -> {self.children}"


class Tree:
    """
    Tree data structure.

    Parameters
    ----------
    nodes : Dict[str, Node]
        Lookup table for nodes.
    name : Optional[str]
        Name of the tree, default value `'-'.join(roots)`.

    Attributes
    ----------
    roots : List[str]
        List of roots.
    atom_label : Dict[str, int]
        Atom name to int label (0...n_atoms -1).
    node_label : Dict[str, int]
        Node name to overall int label (0...n_nodes-1).
    node_level : Dict[str, int]
        Lookup table of node level.
    levels : List[Set[str]]
        List of levels of nodes.
    name : str
        Name of the tree
    """

    def __init__(self, nodes: Dict[str, Node], name: Optional[str] = None):
        """
        Init tree object.

        Parameters
        ----------
        nodes : Dict[str, Node]
            Lookup table for nodes.
        name : Optional[str]
            Name of the tree, default value `'-'.join(roots)`.
        """

        _roots = [v for k, v in nodes.items() if v.is_root]
        _roots.sort(key=lambda x: -len(x.atoms))
        self.roots = [n.name for n in _roots]

        _atoms = [v for k, v in nodes.items() if v.is_atom]
        _atoms.sort(key=lambda x: str(x))
        self.atom_label = {a.name: i for i, a in enumerate(_atoms)}

        _node = [n for n in nodes.values()]
        _node.sort(key=lambda x: str(x))
        self.node_label = {n.name: i for i, n in enumerate(_node)}

        self.name = name if name else "-".join(self.roots)

        self.__nodes = nodes

        node_level, levels = index_nodes_by_level(nodes)
        self.node_level = node_level
        self.levels = levels

    @property
    def nodes(self) -> Dict[str, Node]:
        """
        Short summary.

        Returns
        -------
        Dict[str, Node]
            Return nodes, making it read-only.
        """
        return self.__nodes

    def subtree_nodes(self, root: str) -> Dict[str, Node]:
        """
        Get nodes of the subtree at `root`.

        Parameters
        ----------
        root : str
            Name of root.

        Returns
        -------
        Dict[str, Node]
            Lookup table of subtree nodes.
        """
        return {n: self.nodes[n] for n in all_leaf_nodes(root, self.nodes)}

    def subtree(self, root: str) -> "Tree":
        """
        Generate subtree at `root`.

        Parameters
        ----------
        root : str
            Name of root.

        Returns
        -------
        Tree
            Subtree at `root`.
        """
        nodes = deepcopy(self.subtree_nodes(root))
        nodes[root].parent = None
        return Tree(nodes)

    def to_dict(self) -> Dict[str, str]:
        """
        Serialize the tree to dictionary, i.e. child-parent map.

        Returns
        -------
        Dict[str, str]
            Child-parent map.
        """

        child_to_parent = dict()

        for name, node in self.nodes.items():
            child_to_parent[name] = node.parent

        return child_to_parent

    def to_yaml(self) -> str:
        """
        Serialize the tree to yaml string.

        Returns
        -------
        str
            Yaml string of child-parent map.
        """
        return yaml.dump(self.to_dict())

    @classmethod
    def from_dict(cls, child_to_parent: Dict[str, str]) -> "Tree":
        """
        Build tree from child-parent map.

        Parameters
        ----------
        child_to_parent : Dict[str, str]
            Child-parent map.

        Returns
        -------
        Tree
            Tree object.
        """
        nodes = build_nodes(child_to_parent)
        push_atoms(nodes)
        return cls(nodes)

    @classmethod
    def from_yaml(cls, yaml_string: str) -> "Tree":
        """
        Build tree from yaml string.

        Parameters
        ----------
        yaml_string : str
            Yaml string of child-parent map.

        Returns
        -------
        Tree
            Tree object.
        """
        return cls.from_dict(yaml.safe_load(yaml_string))
