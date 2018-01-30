#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 11/15/17 7:38 PM
# @Author  : Xin He

from numpy import *


def load_simp_data():
    data_mat = matrix( [[1., 2.1],
                       [2., 1.1],
                       [1.3, 1.],
                       [1., 1],
                       [2., 1.]])

    class_labels = [1.0, 1.0, -1.0, -1.0, 1.0]

    return data_mat, class_labels


