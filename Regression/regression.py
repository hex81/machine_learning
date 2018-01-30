#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 11/19/17 11:47 PM
# @Author  : Xin He


from numpy import *


def load_data_set(file_name):
    # num_feature = len(open(file_name).readline().split("\t")) - 1
    data_matrix = []
    label_matrix = []

    with open(file_name) as fr:
        for line in fr.readlines():
            line_list = map(float, line.strip().split("\t"))
            data_matrix.append(line_list[:-1])
            label_matrix.append(line_list[-1])

    return data_matrix, label_matrix


def stand_regress(x_arr, y_arr):
    x_mat = mat(x_arr)
    y_mat = mat(y_arr).T
    x_t_x = x_mat.T * x_mat
    if linalg.det(x_t_x) == 0:
        print "This matrix is singular, can't do inverse"
        return

    ws = x_t_x.I * (x_mat.T * y_mat)

    return ws


def lwlr(test_data, x_arr, y_arr, k=1.0):
    x_matrix = mat(x_arr)
    y_matrix = mat(y_arr).T

    m, n = shape(x_matrix)
    weights = mat(eye((m)))

    for i in xrange(m):
        diff_data = test_data - x_matrix[i]
        weights[i, i] = exp(diff_data * diff_data.T / (-2 * k**2))

    x_t_x = x_matrix.T * weights * x_matrix
    if linalg.det(x_t_x) == 0.0:
        print "This matrix is singular, can't do inverse"
        return

    ws = x_t_x.I * x_matrix.T * weights * y_matrix

    return test_data * ws


def lwlr_test(test_arr, x_arr, y_arr, k=1.0):
    m, n = shape(test_arr)
    y_hat = zeros(m)

    for i in xrange(m):
        y_hat[i] = lwlr(test_arr[i], x_arr, y_arr, k)

    return y_hat


def rss_error(y_arr, y_hat_arr):
    return ((y_arr - y_hat_arr)**2).sum()


def ridge_regres(x_mat, y_mat, lam=0.2):
    x_t_x = x_mat.T * x_mat
    denom = x_t_x + eye(shape(x_mat)[1]) * lam
    if linalg.det(denom) == 0.0:
        print "This matrix is singular."
        return

    ws = denom.I * x_mat.T * y_mat

    return ws


def ridge_test(x_arr, y_arr):
    x_mat = mat(x_arr)
    y_mat = mat(y_arr).T

    x_mean = mean(x_mat, 0)
    y_mean = mean(y_mat, 0)

    x_var = var(x_mat, 0)
    y_var = var(y_mat, 0)

    x_mat = (x_mat - x_mean) / x_var
    y_mat = (y_mat - y_mean) / y_var

    num_test = 30
    w_mat = zeros((num_test, shape(x_mat)[1]))
    for i in xrange(num_test):
        ws = ridge_regres(x_mat, y_mat, exp(i-10))
        w_mat[i, :] = ws.T

    return w_mat


def stage_wise(x_arr, y_arr, eps=0.01, iter=100):
    x_mat = mat(x_arr)
    y_mat = mat(y_arr).T

    y_mean = mean(y_mat, 0)
    x_mean = mean(x_mat, 0)

    y_mat = y_mat - y_mean
    x_var = var(x_mat, 0)

    x_mat = (x_mat - x_mean) / x_var

    m, n = shape(x_mat)
    return_mat = zeros((iter, n))

    ws = zeros((n, 1))
    # ws_test = ws.copy()
    # ws_max = ws.copy()

    for i in xrange(iter):
        min_error = inf
        for j in xrange(n):
            for sig in [-1, 1]:
                ws_test = ws.copy()
                ws_test[j] += eps * sig
                y_test = x_mat * ws_test
                rss_e = rss_error(y_mat.A, y_test.A)

                if rss_e < min_error:
                    min_error = rss_e
                    ws_max = ws_test

        ws = ws_max.copy()
        return_mat[i, :] = ws.T

    return return_mat
