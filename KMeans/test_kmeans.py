#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 11/29/17 12:18 AM
# @Author  : Xin He


import kmeans

from numpy import *


# data_mat = mat(kmeans.load_data_set('testSet.txt'))
# # centroids = kmeans.rand_cent(data_mat, 2)
# # distant = kmeans.dist_vec(data_mat[0], data_mat[1])
# # print distant[0, 0]
#
# centroids, classify_record = kmeans.k_means(data_mat, 2)
# print centroids
# # print classify_record
#
# data_mat_3 = mat(kmeans.load_data_set('testSet2.txt'))
# centroid_list, new_assessment = kmeans.bi_k_means(data_mat_3, 3)
# print centroid_list

response = kmeans.geo_grab('1 VA Center', 'Augusta, ME')
