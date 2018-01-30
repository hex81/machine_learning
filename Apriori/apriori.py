#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 12/11/17 12:47 AM
# @Author  : Xin He


def load_data():
    return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]


def create_item_set(data_set):
    item_set = []
    for transaction in data_set:
        for item in transaction:
            if not [item] in item_set:
                item_set.append([item])

    item_set.sort()
    # print item_set

    return map(frozenset, item_set)


def scan_data(data_set, item_list, min_support):
    item_count = dict()
    for transaction in data_set:
        for item in item_list:
            if item.issubset(transaction):
                if item not in item_count:
                    item_count[item] = 1
                else:
                    item_count[item] += 1

    support_list = list()
    support_data = dict()
    for key in item_count:
        support = item_count[key] / float(len(data_set))
        if support >= min_support:
            support_list.insert(0, key)

        support_data[key] = support

    return support_list, support_data


def apriori_gen(item_list, k):
    support_list = []
    len_lk = len(item_list)

    for i in xrange(len_lk):
        for j in xrange(i+1, len_lk):
            l_1 = list(item_list[i])[:k-2]
            l_2 = list(item_list[j])[:k-2]
            l_1.sort()
            l_2.sort()

            if l_1 == l_2:
                support_list.append(item_list[i] | item_list[j])

    return support_list


def apriori(data_set, min_support=0.5):
    init_item_set = create_item_set(data_set)
    d_set = map(set, data_set)
    init_support_list, init_support_data = scan_data(d_set,
                                                     init_item_set,
                                                     min_support)
    support_list = [init_support_list]
    k = 2

    while len(support_list[k-2]) > 0:
        item_set_k = apriori_gen(support_list[k-2], k)
        support_list_k, support_data = scan_data(d_set, item_set_k, min_support)
        init_support_data.update(support_data)
        support_list.append(support_list_k)
        k += 1

    return support_list, init_support_data




