# -*- coding: utf-8 -*-

def to_tree(my_dict):
    tree = {}

    build_tree(tree, None, my_dict)
    return tree

def build_tree(tree, parent, nodes):
    children = [n for n in nodes if n.parentId == parent]
    for child in children:
        tree[child]['children'] = {}
        build_tree(tree[child], child, nodes)
