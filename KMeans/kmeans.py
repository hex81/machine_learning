#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 11/28/17 1:28 AM
# @Author  : Xin He

from numpy import *
import requests
import json
import time


def load_data_set(file_name):
    data_list = []
    with open(file_name) as fr:
        for line in fr.readlines():
            features = map(float, line.strip().split("\t"))
            data_list.append(features)

    return data_list


def dist_vec(vec_a, vec_b):
    return sqrt(sum(power(vec_a - vec_b, 2)))
    # return sqrt((vec_a - vec_b) * (vec_a - vec_b).T)


def rand_cent(data_set, k):
    n = shape(data_set)[1]
    centroids = mat(zeros((k, n)))

    for j in xrange(n):
        min_j = min(data_set[:, j])
        range_j = float(max(data_set[:, j]) - min_j)
        centroids[:, j] = min_j + range_j * random.rand(k, 1)

    return centroids


def k_means(data_set, k):
    m, n = shape(data_set)
    cluster_assment = mat(zeros((m, 2)))
    centroids = rand_cent(data_set, k)
    centroids_change = True
    while centroids_change:
        centroids_change = False
        for row in xrange(m):
            min_dis = inf
            label = -1
            for i in xrange(k):
                dis = dist_vec(data_set[row, :], centroids[i, :])
                if dis < min_dis:
                    min_dis = dis
                    label = i
            if cluster_assment[row, 0] != label:
                centroids_change = True

            cluster_assment[row, :] = label, min_dis**2

        for classify in xrange(k):
            sub_data = data_set[nonzero(cluster_assment[:, 0].A == classify)[0]]
            # print sub_data
            centroids[classify, :] = mean(sub_data, axis=0)

    return centroids, cluster_assment


def bi_k_means(data_set, k):
    m, n = shape(data_set)
    cluster_assessment = mat(zeros((m, 2)))
    centroid_0 = mean(data_set, axis=0).tolist()
    centroid_list = list()
    centroid_list.append(centroid_0)

    for i in xrange(m):
        cluster_assessment[i, 1] = dist_vec(mat(centroid_0), data_set[i, :])**2

    while len(centroid_list) < k:
        lowest_sse = inf
        for i in xrange(len(centroid_list)):
            sub_data = data_set[nonzero(cluster_assessment[:, 0].A == i)[0]]
            centroid_m, cur_cluster_ass = k_means(sub_data, 2)
            sse_split = sum(cur_cluster_ass[:, 1])
            sse_no_split = sum(cluster_assessment[nonzero(cluster_assessment[:, 0].A != i)[0], 1])

            print "sse is : {}, no split sse is {}".format(sse_split,
                                                           sse_no_split)

            if (sse_split + sse_no_split) < lowest_sse:
                best_centroid_spit = i
                best_centroid = centroid_m
                best_cluster_ass = cur_cluster_ass.copy()
                lowest_sse = sse_no_split + sse_split

        best_cluster_ass[nonzero(best_cluster_ass[:, 0].A == 1)[0], 0] = \
            len(centroid_list)

        best_cluster_ass[nonzero(best_cluster_ass[:, 0].A == 0)[0], 0] = \
            best_centroid_spit

        centroid_list[best_centroid_spit] = best_centroid[0, :]
        centroid_list.append(best_centroid[1, :])

        cluster_assessment[nonzero(cluster_assessment[:, 0].A ==
                                   best_centroid_spit)[0], :] = best_cluster_ass

    return centroid_list, cluster_assessment


def geo_grab(st_address, city):
    url = 'http://where.yahooapis.com/geocode'
    params = dict()
    params['flags'] = 'J'
    params['appid'] = 'ppp68N8t'
    params['location'] = "{} {}".format(st_address, city)

    resp = requests.get(url, params)

    return resp.json()



