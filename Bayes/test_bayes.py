#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 9/21/17 9:07 AM
# @Author  : Xin He


import bayes
import feedparser


# data_set, classes = bayes.load_data_set()
# vocab_list = bayes.create_vocab_list(data_set)
# vec = bayes.set_words_vec(vocab_list, data_set[0])
#
# # print data_set
# # print classes
# print vocab_list
# # print vec
#
#
# train_matrix = [bayes.set_words_vec(vocab_list, doc) for doc in data_set]
# p1_v, p0_v, p_b = bayes.train_nbayes(train_matrix, classes)
# print p1_v
# print p0_v
# print p_b

# bayes.testing_nb()

# bayes.spam_test()
ny = feedparser.parse('http://newyork.craigslist.org/stp/index.rss')
sf = feedparser.parse('http://sfbay.craigslist.org/stp/index.rss')
# for i in xrange(10):
#     vocabs, p_sf, p_ny = bayes.local_words(ny, sf)
#     print vocabs
#     print p_sf
#     print p_ny

bayes.get_top_words(ny, sf)
