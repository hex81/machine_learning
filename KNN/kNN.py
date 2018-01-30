#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 9/4/17 11:46 PM
# @Author  : Xin He

import os

from numpy import *
import operator


def create_data_set():
    group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels


def file2matrix(filename):
    """

    Args:
        filename: original data file

    Returns:
        t_matrix: training data matrix
        y_labels: training labels
    """

    with open(filename, 'r') as fr:
        data_lines = fr.readlines()

    row_m = len(data_lines)
    column_n = len(data_lines[0].split("\t")) - 1
    print "training data matrix is: {} * {}".format(row_m, column_n)

    t_matrix = zeros((row_m, column_n))
    y_labels = []

    index = 0
    for line in data_lines:
        list_line = line.strip().split("\t")
        t_matrix[index, :] = list_line[0:column_n]
        y_labels.append(int(list_line[-1]))
        index += 1

    return t_matrix, y_labels


def auto_norm(data_set):
    """
    Norm original data set
    Args:
        data_set: original data set

    Returns:
        norm_set, ranges, min_val
    """
    min_val = data_set.min(0)
    max_val = data_set.max(0)
    ranges = max_val - min_val

    # norm_set = zeros(shape(data_set))
    row_m = data_set.shape[0]
    norm_set = data_set - tile(min_val, (row_m, 1))
    norm_set = norm_set / tile(ranges, (row_m, 1))

    return norm_set, ranges, min_val


def classify(input_x, data_set, labels, k=10):
    """
    Classify x
    Args:
        input_x: input data
        data_set:
        labels:
        k:

    Returns:
        class label
    """

    row_m = data_set.shape[0]
    deviation = data_set - tile(input_x, (row_m, 1))
    var_diff = deviation ** 2
    dis_array = var_diff.sum(axis=1)
    dev = dis_array ** 0.5

    # get sorted distance index array
    sorted_dis_index = dev.argsort()
    label_count = {}
    for i in range(k):
        # get index's label
        label = labels[sorted_dis_index[i]]
        label_count[label] = label_count.get(label, 0) + 1
    sorted_label_count = sorted(label_count.items(), key=operator.itemgetter(1),
                                reverse=True)

    return sorted_label_count[0][0]


def dating_class_test():
    """
    Test classify effect
    Returns:

    """

    ratio = 0.1
    k = 10
    error_ratio = 0.0

    dating_x, dating_labels = file2matrix("datingTestSet2.txt")
    norm_data_x, ranges, min_val = auto_norm(dating_x)
    row_m = norm_data_x.shape[0]
    test_row = int(row_m * ratio)

    for i in xrange(test_row):
        label = classify(norm_data_x[i, :], norm_data_x[test_row:row_m, :],
                         dating_labels[test_row:row_m], k)

        print "Data is labeled {}, " \
              "the real answer is {}".format(label, dating_labels[i])

        if label != dating_labels[i]:
            error_ratio += 1

    print "the total error rate is: {}".format(error_ratio / float(test_row))


def classify_person():
    result_class = ['not at all', 'in small does', 'in large does']
    k = 3
    percent_tats = float(raw_input("Input percentage of time spending on game: "))
    flight_miles = float(raw_input("Input flight miles per year: "))
    ice_cream = float(raw_input("Input ice cream consuming per year: "))

    dating_x, dating_labels = file2matrix("datingTestSet2.txt")
    norm_data_x, ranges, min_val = auto_norm(dating_x)
    input_data = array([flight_miles, percent_tats, ice_cream])
    norm_input = (input_data - min_val) / ranges
    classify_result = classify(norm_input, norm_data_x, dating_labels, k)

    print "This person is: {}".format(result_class[classify_result-1])


def img2vector(filename):
    """
    convert 32*32 img to vector
    Args:
        filename: 32*32 img file

    Returns:
        img_vector
    """
    img_vector = zeros((1, 32*32))
    with open(filename, 'r') as fr:
        for row in xrange(32):
            line = fr.readline()
            for column in xrange(32):
                img_vector[0, 32*row+column] = int(line[column])

        return img_vector


def handwriting_class_test():
    """

    Returns:

    """

    training_mat, hw_labels = load_data()

    ratio = test_handwriting(training_mat, hw_labels)

    print "The error ratio is: {}".format(ratio)


def load_data():
    """
    load training data from trainingDigits
    Returns:

    """

    training_files_dir = "digits/trainingDigits"
    training_files = os.listdir(training_files_dir)
    file_num = len(training_files)
    hw_labels = []

    training_mat = zeros((file_num, 32 * 32))
    for i in xrange(file_num):
        filename = training_files[i]
        file_label = int((filename.split(".")[0]).split("_")[0])
        hw_labels.append(file_label)
        training_mat[i, :] = img2vector(training_files_dir + '/' + filename)

    return training_mat, hw_labels


def test_handwriting(training_mat, hw_labels):
    """
    test handwriting digit in testDigits.
    Args:
        training_mat:
        hw_labels:

    Returns:

    """

    test_files_dir = "digits/testDigits"
    test_files = os.listdir(test_files_dir)
    file_num = len(test_files)
    error = 0.0

    for i in xrange(file_num):
        filename = test_files[i]
        file_label = int((filename.split(".")[0]).split("_")[0])
        test_vector = img2vector(test_files_dir + '/' + filename)
        test_label = classify(test_vector, training_mat, hw_labels)

        if file_label != test_label:
            print "file label is:{},test label is:{}".format(file_label,
                                                             test_label)
            print "file name is: {}".format(filename)
            error += 1

    print "The total number of errors is: {}".format(error)

    return float(error / file_num)







