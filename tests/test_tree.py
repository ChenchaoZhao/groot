import os

import yaml

import groot

pwd = os.path.dirname(__file__)

with open(os.path.join(pwd, "test_data.yaml"), "r") as f:
    trees = yaml.safe_load(f.read())


def test_load_from_dict():

    for k, v in trees.items():
        groot.Tree.from_dict(v)


def test_load_from_yaml():

    for k, v in trees.items():
        groot.Tree.from_yaml(yaml.dump(v))


def test_dump_to_dict():

    for k, v in trees.items():
        assert groot.Tree.from_dict(v).to_dict() == v


def test_dump_to_yaml():

    for k, v in trees.items():
        assert groot.Tree.from_yaml(yaml.dump(v)).to_yaml() == yaml.dump(v)


def test_atoms():

    t = groot.Tree.from_dict(trees["tree-0"])
    assert t.atom_label == {"a.a": 0, "a.b": 1}


def test_roots():

    assert groot.Tree.from_dict(trees["tree-0"]).roots == ["a"]
    assert groot.Tree.from_dict(trees["tree-1"]).roots == ["a"]
    assert groot.Tree.from_dict(trees["tree-2"]).roots == ["a", "b"]


def test_levels():

    assert len(groot.Tree.from_dict(trees["tree-0"]).levels) == 2
    assert len(groot.Tree.from_dict(trees["tree-1"]).levels) == 3
    assert len(groot.Tree.from_dict(trees["tree-2"]).levels) == 3


def test_subtree():

    assert (
        groot.Tree.from_dict(trees["tree-2"]).subtree("a").nodes
        == groot.Tree.from_dict(trees["tree-1"]).nodes
    )
