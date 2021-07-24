r"""
The package helps manage hierarchical concept trees.

Each tree is serialized as a yaml file which can be loaded to construct the python
class.
"""

__version__ = "0.1.0"

from . import functional, tree, utils
from .tree import Tree
