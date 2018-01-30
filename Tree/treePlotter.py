#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 9/14/17 12:41 AM
# @Author  : Xin He

import matplotlib.pyplot as plt


decisionNode = dict(boxstyle="sawtooth", fc="0.8")
leafNode = dict(boxstyle="round4", fc="0.8")
arrow_args = dict(arrowstyle="<-")


def plot_node(node_txt, center_pt, parent_pt, node_type):
    create_plot.ax1.annotate(node_txt, xy=parent_pt, xycoords='axes fraction',
                             xytext=center_pt, textcoords='axes fraction',
                             va="center", ha="center", bbox=node_type,
                             arrowprops=arrow_args)


def create_plot(tree):
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    axprops = dict(xticks=[], yticks=[])
    create_plot.ax1 = plt.subplot(111, frameon=False, **axprops)
    plot_tree.totalW = float(get_num_leaf(tree))
    plot_tree.totalD = float(get_depth_tree(tree))
    plot_tree.xOff = -0.5 / plot_tree.totalW
    plot_tree.yOff = 1.0
    plot_tree(tree, (0.5, 1.0), '')

    # plot_node("decision node", (0.5, 0.1), (0.1, 0.5), decisionNode)
    # plot_node("leaf node", (0.8, 0.1), (0.3, 0.8), leafNode)
    plt.show()


def get_num_leaf(tree):
    """
    Get num of leaves of the tree
    Args:
        tree: decision tree

    Returns:
        num_leaf

    """

    num_leaf = 0

    root = tree.keys()[0]
    branches = tree[root]
    for key in branches.keys():
        if isinstance(branches[key], dict):
            num_leaf += get_num_leaf(branches[key])
        else:
            num_leaf += 1

    return num_leaf


def get_depth_tree(tree):
    """
    Get the depth of the tree
    Args:
        tree: decision tree

    Returns:
        return max_depth

    """

    max_depth = 0

    root = tree.keys()[0]
    branches = tree[root]
    for key in branches.keys():
        if isinstance(branches[key], dict):
            depth = 1 + get_depth_tree(branches[key])
        else:
            depth = 1

    if depth > max_depth:
        max_depth = depth

    return max_depth


def plot_mid_text(cnt_pt, parent_pt, txt):
    x_mid = (parent_pt[0] - cnt_pt[0]) / 2.0 + cnt_pt[0]
    y_mid = (parent_pt[1] - cnt_pt[1]) / 2.0 + cnt_pt[1]
    create_plot.ax1.text(x_mid, y_mid, txt)


def plot_tree(tree, parent_pt, node_txt):
    num_leaf = get_num_leaf(tree)
    depth = get_depth_tree(tree)
    root = tree.keys()[0]
    cnt_pt = (plot_tree.xOff + (1 + float(num_leaf))/2/plot_tree.totalW,
              plot_tree.yOff)

    plot_mid_text(cnt_pt, parent_pt, node_txt)
    plot_node(root, cnt_pt, parent_pt, decisionNode)
    branches = tree[root]
    plot_tree.yOff = plot_tree.yOff - 1.0 / plot_tree.totalD
    for key in branches.keys():
        if isinstance(branches[key], dict):
            plot_tree(branches[key], cnt_pt, str(key))
        else:
            plot_tree.xOff = plot_tree.xOff + 1.0 / plot_tree.totalW
            plot_node(branches[key], (plot_tree.xOff, plot_tree.yOff),
                      cnt_pt, leafNode)
            plot_mid_text((plot_tree.xOff, plot_tree.yOff), cnt_pt, str(key))

    plot_tree.yOff = plot_tree.yOff + 1.0 / plot_tree.totalD

