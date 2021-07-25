"""
The package helps manage hierarchical concept trees.

Each tree can be serialized as a yaml file and each file can be loaded to
construct the python class.

Goals
-----
* Save the trees in most compact format
* Be able to load the trees from serialized files
* List all nodes
* List nodes on a given depth
* List all atomic nodes
"""

__version__ = "0.1.0"

from . import functional, tree, utils
from .tree import Tree
