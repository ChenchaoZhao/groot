# Groot
[![test](https://github.com/ChenchaoZhao/groot/actions/workflows/lint-test.yaml/badge.svg)](https://github.com/ChenchaoZhao/groot/actions/workflows/lint-test.yaml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://pypip.in/v/i-am-groot/badge.png)](https://pypi.python.org/pypi/i-am-groot)

Manage hierarchical concept trees with style

## Install
```pip install i-am-groot```

## Goals
* Save the trees in most compact format
* Be able to load the trees from serialized files
* List all nodes
* List nodes on a given depth
* List all atomic nodes

## Example
```python
import groot

tree = groot.Tree.from_yaml(serialized_file)
print(groot.utils.draw_tree(tree, show_level=True))

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
