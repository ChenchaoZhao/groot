from dataclasses import *
from typing import *


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
