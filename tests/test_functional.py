import os

import yaml

import groot.functional as F

pwd = os.path.dirname(__file__)

with open(os.path.join(pwd, "test_data.yaml"), "r") as f:
    trees = yaml.safe_load(f.read())


def test_build_nodes():
    print(F.build_nodes(trees["tree-0"]))


def test_push_atoms():
    nodes = F.build_nodes(trees["tree-0"])
    F.push_atoms(nodes)


def test_get_leaf():
    nodes = F.build_nodes(trees["tree-2"])
    F.push_atoms(nodes)
    assert F.all_leaf_nodes("a", nodes) == set(["a", "a.a", "a.b", "a.a.a"])

    nodes = F.build_nodes(trees["tree-2"])
    F.push_atoms(nodes)
    assert F.all_leaf_nodes("a.a", nodes) == set(["a.a", "a.a.a"])


def test_levels():
    nodes = F.build_nodes(trees["tree-0"])
    F.push_atoms(nodes)
    print(F.index_nodes_by_level(nodes))
