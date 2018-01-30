#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 11/15/17 9:35 PM
# @Author  : Xin He

from numpy import *

import adaboost
import boost


data_mat, class_labels = adaboost.load_simp_data()

# print data_mat
# print class_labels

# D = mat(ones((5, 1))/5)
# best_strump, min_error, best_class = boost.build_stump(data_mat, class_labels, D)
# print best_strump
# print min_error
# print best_class

weak_class_arr = boost.ada_boost_train_ds(data_mat, class_labels)

# print weak_class_arr

boost.ada_classify([[0, 0], [1, 2]], weak_class_arr)
