#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 12/11/17 1:29 AM
# @Author  : Xin He


import apriori


print "1. load data........."
data_set = apriori.load_data()
print data_set

print "2. create item set..."
item_set = apriori.create_item_set(data_set)
print item_set

print "3. get support list & support data"
support_list, support_data = apriori.scan_data(map(set, data_set),
                                               item_set, 0.5)

print support_list
print support_data

print "4. get all support list & support data"
support_list, support_data = apriori.apriori(data_set)
print support_list
print support_data

