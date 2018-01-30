#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 9/12/17 8:18 PM
# @Author  : Xin He

import trees
import treePlotter


def create_data_set():
    data = [[1, 1, 'yes'],
            [1, 1, 'yes'],
            [0, 1, 'no'],
            [1, 0, 'no'],
            [1, 0, 'no']]

    label = ['no surfacing', 'flippers']
    return data, label


if __name__ == '__main__':

    # data_set, labels = create_data_set()
    # entropy = trees.calc_shannon_ent(data_set)
    # split_set = trees.split_data_set(data_set, 0, 0)
    # print "split 0 on value 0: "
    # print split_set
    # split_set = trees.split_data_set(data_set, 0, 1)
    # print "split 0 on value 1: "
    # print split_set
    #
    # best_feature = trees.choose_best_feature_split(data_set)
    # print "best split feature is: {}".format(best_feature)
    #
    # print trees.majority_cnt([1, 0, 0, 2, 3, 4])

    # decision_tree = trees.create_tree(data_set, labels[:])
    # print "Decision Tree is: {}".format(decision_tree)

    # treePlotter.create_plot(decision_tree)
    # print treePlotter.get_num_leaf(decision_tree)
    # print treePlotter.get_depth_tree(decision_tree)
    # print trees.classify(decision_tree, labels[:], [0, 1])

    # trees.store_tree(data_set, "dataSet.txt")
    # trees.store_tree(decision_tree, "decision_tree.txt")
    # print trees.grab_tree("dataSet.txt")
    # print trees.grab_tree("decision_tree.txt")

    lenses_tree = trees.create_test_lens()
    print lenses_tree
    treePlotter.create_plot(lenses_tree)
