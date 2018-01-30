#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 11/20/17 1:00 AM
# @Author  : Xin He


import regression
from numpy import *
import matplotlib.pyplot as plt


x_arr, y_arr = regression.load_data_set('ex0.txt')
# print "================ x array is :============"
# print x_arr[0:2]
# # print "================ y array is :============"
# print y_arr
#
# ws = regression.stand_regress(x_arr, y_arr)
# # print "================== ws ==================="
# print ws
#
x_mat = mat(x_arr)
y_mat = mat(y_arr)
#
fig = plt.figure()
ax = fig.add_subplot(111)
#
# # ax.scatter(x_mat[:, 1].flatten().A[0], y_mat.T[:, 0].flatten().A[0])
#
# x_copy = x_mat.copy()
# x_copy.sort(0)
# y_hat = x_copy * ws
# ax.plot(x_copy[:, 1], y_hat)
# plt.show()

# print corrcoef(y_hat.T, y_mat)

# print regression.lwlr(x_arr[0], x_arr, y_arr, 0.05)
# print regression.lwlr(x_arr[1], x_arr, y_arr, 0.05)
# y_hat = regression.lwlr_test(x_arr, x_arr, y_arr, 0.003)
#
# srt_ind = x_mat[:, 1].argsort(0)
# x_sort = x_mat[srt_ind][:, 0, :]
# ax.plot(x_sort[:, 1], y_hat[srt_ind])
# ax.scatter(x_mat[:, 1].flatten().A[0], mat(y_arr).T.flatten().A[0], s=2, c='red')
# plt.show()
#
#
ab_x, ab_y = regression.load_data_set('abalone.txt')
# y_hat_01 = regression.lwlr_test(ab_x[0:99], ab_x[0:99], ab_y[0:99], 0.1)
# y_hat_1 = regression.lwlr_test(ab_x[0:99], ab_x[0:99], ab_y[0:99], 1)
# y_hat_10 = regression.lwlr_test(ab_x[0:99], ab_x[0:99], ab_y[0:99], 10)
#
# print y_hat_01
# print y_hat_1
# print y_hat_10
#
# print regression.rss_error(ab_y[0:99], y_hat_01.T)
# print regression.rss_error(ab_y[0:99], y_hat_1.T)
# print regression.rss_error(ab_y[0:99], y_hat_10.T)

ridge_weights = regression.ridge_test(ab_x, ab_y)
stage_weights = regression.stage_wise(ab_x, ab_y, 0.001, 5000)

weights = regression.stand_regress(ab_x, ab_y)

# ax.plot(ridge_weights)
ax.plot(stage_weights)
plt.show()

print stage_weights
print weights.T
