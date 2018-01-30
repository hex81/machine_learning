#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 9/5/17 1:27 AM
# @Author  : Xin He

from numpy import *
import kNN
import matplotlib
import matplotlib.pyplot as plt

if __name__ == '__main__':
    # X, y = kNN.file2matrix("datingTestSet2.txt")
    # print "Training X is:\n {}".format(X)
    # print "Training y is:\n {}".format(y)
    # print "Array y is:\n {}".format(array(y))
    #
    # norm_X, ranges, min_val = kNN.auto_norm(X)
    # print norm_X
    # print ranges
    # print min_val

    # kNN.dating_class_test()
    # kNN.classify_person()

    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # ax.scatter(X[:, 0], X[:, 1], 15*array(y), 15*array(y))
    # plt.show()

    # test_vector = kNN.img2vector("digits/testDigits/0_8.txt")
    # print test_vector[0, 32:63]

    kNN.handwriting_class_test()

