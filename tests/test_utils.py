import os

import yaml

import groot

pwd = os.path.dirname(__file__)

with open(os.path.join(pwd, "test_data.yaml"), "r") as f:
    trees = yaml.safe_load(f.read())


def test_draw():

    for k, v in trees.items():
        tree = groot.Tree.from_dict(v)
        groot.utils.draw_tree(tree)
