#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 9/12/17 7:50 PM
# @Author  : Xin He

import pickle

from math import log
from collections import Counter


def calc_shannon_ent(data_set):
    """
    Calculate Shannon entropy
    Args:
        data_set: data set

    Returns:
        shannon_ent

    """

    num_sample = len(data_set)
    shannon_ent = 0.0

    label_count = {}
    for feature in data_set:
        label = feature[-1]

        if label not in label_count.keys():
            label_count[label] = 1
        else:
            label_count[label] += 1

    for key in label_count:
        prob = float(label_count[key]) / num_sample
        shannon_ent -= prob * log(prob, 2)

    return shannon_ent


def split_data_set(data_set, item, value):
    """
    Split data set
    Args:
        data_set: data set
        item: feature to be split based on this item
        value: feature value

    Returns:
        split_set

    """

    split_set = []

    if item < 0:
        split_set = data_set
    else:
        for feature in data_set:
            if feature[item] == value:
                reduced_feature = feature[:item]
                reduced_feature.extend(feature[item+1:])
                split_set.append(reduced_feature)

    return split_set


def choose_best_feature_split(data_set):
    """
    choose best split base on shannon entropy
    Args:
        data_set: data set

    Returns:
        best_feature

    """

    num_feature = len(data_set[0]) - 1

    # initial best info gain
    best_info_gain = 0.0

    # default best split feature is -1, data set doesn't need to be split
    best_feature = -1

    # calc base entropy with whole data_set
    base_entropy = calc_shannon_ent(data_set)

    for i in xrange(num_feature):
        features = [sample[i] for sample in data_set]
        unique_feature = set(features)
        total_entropy = 0.0
        for value in unique_feature:
            split_data = split_data_set(data_set, i, value)
            # prob must be a float number
            prob = len(split_data) / float(len(data_set))
            # calc total entropy of split_data
            total_entropy += prob * calc_shannon_ent(split_data)

        info_gain = base_entropy - total_entropy
        if info_gain > best_info_gain:
            best_info_gain = info_gain
            best_feature = i

    return best_feature


def majority_cnt(class_list):
    """
    find majority class
    Args:
        class_list: class list

    Returns:
        majority class

    """

    class_count = Counter(class_list)
    majority_class = class_count.most_common(1)

    return majority_class[0][0]


def create_tree(data_set, labels):
    """
    create decision tree
    Args:
        data_set: data set
        labels: labels

    Returns:
        decision_tree

    """

    print "data set is: {}".format(data_set)

    class_list = [sample[-1] for sample in data_set]

    if all(x == class_list[0] for x in class_list):
        return class_list[0]

    if len(data_set[0]) == 1:
        return majority_cnt(class_list)

    best_feature = choose_best_feature_split(data_set)

    # if data set shouldn't be split, choose majority count
    if best_feature == -1:
        return majority_cnt(class_list)

    print "Best feature is: {}".format(best_feature)
    print "labels is: {}".format(labels)

    best_feature_label = labels[best_feature]
    decision_tree = {best_feature_label: {}}
    feature_values = [sample[best_feature] for sample in data_set]

    del(labels[best_feature])
    # sub_labels = labels[:]
    for value in set(feature_values):
        # sub_labels will be modified by create_tree
        # each value should use the same labels copy.
        sub_labels = labels[:]
        split_data = split_data_set(data_set, best_feature, value)
        decision_tree[best_feature_label][value] = create_tree(split_data,
                                                               sub_labels)

    return decision_tree


def classify(tree, labels, test_vec):
    """
    Classify test vector
    Args:
        tree:
        labels:
        test_vec:

    Returns:
        label

    """

    root_key = tree.keys()[0]
    branches = tree[root_key]
    print labels
    root_key_index = labels.index(root_key)

    for key in branches:
        if test_vec[root_key_index] == key:
            if isinstance(branches[key], dict):
                label = classify(branches[key], labels, test_vec)
            else:
                label = branches[key]

    return label


def store_tree(tree, filename):
    fw = open(filename, 'w')
    pickle.dump(tree, fw)
    fw.close()


def grab_tree(filename):
    fr = open(filename, 'r')
    return pickle.load(fr)


def create_test_lens():

    lenses = []
    with open('lenses.txt') as fr:
        for line in fr.readlines():
            lenses.append(line.strip().split('\t'))

    print lenses

    lenses_labels = ['age', 'prescript', 'astigmatic', 'tearRate']
    lenses_tree = create_tree(lenses, lenses_labels)

    return lenses_tree


