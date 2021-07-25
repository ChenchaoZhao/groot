"""
The package helps manage hierarchical concept trees.

Each tree can be serialized as a yaml file and each file can be loaded to
construct the python class `Tree`.

Goals
-----
* Save the trees in most compact format
* Be able to load the trees from serialized files
* List all nodes
* List nodes on a given depth
* List all atomic nodes

Example
-------
```
import groot

tree = groot.Tree.from_yaml(serialized_tree_string)
groot.utils.draw_tree(tree, show_level=True)

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

__version__ = "0.1.3"

from . import functional, tree, utils
from .tree import Tree
