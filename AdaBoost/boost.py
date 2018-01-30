#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 11/15/17 9:39 PM
# @Author  : Xin He

from numpy import *


def stump_classify(data_mat, dimen, thresh_hold, thresh_ineq):
    ret_array = ones((shape(data_mat)[0], 1))
    if thresh_ineq == 'lt':
        ret_array[data_mat[:, dimen] <= thresh_hold] = -1.0
    else:
        ret_array[data_mat[:, dimen] > thresh_hold] = -1.0
    return ret_array


def build_stump(data_arr, class_labels, d):
    data_matrix = mat(data_arr)
    label_mat = mat(class_labels).T
    m, n = shape(data_matrix)
    num_steps = 10.0
    best_stump = {}
    best_class_est = mat(zeros((m, 1)))
    min_error = inf
    for i in range(n):
        range_min = data_matrix[:, i].min()
        range_max = data_matrix[:, i].max()
        step_size = (range_max - range_min) / num_steps
        for j in xrange(-1, int(num_steps)+1):
            for inequal in ['lt', 'gt']:
                thresh_hold = (range_min + float(j) * step_size)
                predicted_val = stump_classify(data_matrix, i, thresh_hold, inequal)
                err_arr = mat(ones((m, 1)))
                err_arr[predicted_val == label_mat] = 0
                weighted_error = d.T * err_arr

                if weighted_error < min_error:
                    min_error = weighted_error
                    best_class_est = predicted_val.copy()
                    best_stump['dim'] = i
                    best_stump['thresh'] = thresh_hold
                    best_stump['ineq'] = inequal

    return best_stump, min_error, best_class_est


def ada_boost_train_ds(data_arr, class_labels, num_iter=40):
    weak_class_att = []
    m, n = shape(data_arr)
    d = mat(ones((m, 1)) / m)
    agg_class_est = mat(zeros((m, 1)))

    for i in xrange(num_iter):
        best_strump, min_error, best_class = build_stump(data_arr,
                                                         class_labels, d)
        alpha = float(0.5 * log((1.0-min_error)/max(min_error, 1e-16)))
        best_strump['alpha'] = alpha
        weak_class_att.append(best_strump)
        expon = multiply(-1*alpha*mat(class_labels).T, best_class)
        d = multiply(d, exp(expon))
        d = d / d.sum()
        print agg_class_est
        agg_class_est += alpha * best_class
        # print "aggregate class est: ", agg_class_est.T
        agg_error = multiply(sign(agg_class_est) != mat(class_labels).T,
                             ones((m, 1)))
        error_rate = agg_error.sum() / m
        # print "total error: {}".format(error_rate)

        if error_rate == 0.0:
            break

    return weak_class_att


def ada_classify(data, classifier_arr):
    data_matrix = mat(data)
    m, n = shape(data_matrix)
    agg_class_est = mat(zeros((m, 1)))
    for i in xrange(len(classifier_arr)):
        class_est = stump_classify(data_matrix, classifier_arr[i]['dim'],
                                   classifier_arr[i]['thresh'],
                                   classifier_arr[i]['ineq'])
        agg_class_est += class_est * classifier_arr[i]['alpha']
        print agg_class_est

    print sign(agg_class_est)

    return sign(agg_class_est)
