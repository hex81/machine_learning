#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 9/21/17 8:26 AM
# @Author  : Xin He

import re
import operator

import feedparser
from numpy import *


def load_data_set():
    posting_list = [
        ['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
        ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
        ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
        ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
        ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
        ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']
    ]

    class_vec = [0, 1, 0, 1, 0, 1]

    return posting_list, class_vec


def create_vocab_list(data_set):
    words_list = []
    for document in data_set:
        words_list.extend(document)

    return list(set(words_list))


def set_words_vec(words_list, input_words):
    vector = [0] * len(words_list)
    for word in input_words:
        if word in words_list:
            vector[words_list.index(word)] = 1

    return vector


def train_nbayes(train_matrix, train_category):
    num_docs = len(train_matrix)
    num_words = len(train_matrix[0])

    p_abusive = sum(train_category) / float(num_docs)

    p1 = ones(num_words)
    p0 = ones(num_words)
    p1_denom = 2.0
    p0_denom = 2.0

    for i in xrange(num_docs):
        if train_category[i] == 1:
            p1 += train_matrix[i]
            p1_denom += sum(train_matrix[i])
        else:
            p0 += train_matrix[i]
            p0_denom += sum(train_matrix[i])

    p1_vec = log(p1 / p1_denom)
    p0_vec = log(p0 / p0_denom)

    return p1_vec, p0_vec, p_abusive


def classify_nb(vec2classify, p0_vec, p1_vec, p_abusive):
    p1 = sum(vec2classify * p1_vec) + log(p_abusive)
    p0 = sum(vec2classify * p0_vec) + (1 - log(p_abusive))

    return 1 if p1 > p0 else 0


def testing_nb():
    data_set, classes = load_data_set()
    vocab_list = create_vocab_list(data_set)

    train_matrix = [set_words_vec(vocab_list, doc) for doc in data_set]
    p1_v, p0_v, p_ab = train_nbayes(train_matrix, classes)
    test_entry = ['love', 'my', 'dalmation']
    doc = array(set_words_vec(vocab_list, test_entry))
    classify = classify_nb(doc, p0_v, p1_v, p_ab)
    print "{} classified as : {}".format(doc, classify)

    test_entry = ['stupid', 'garbage']
    doc = array(set_words_vec(vocab_list, test_entry))
    classify = classify_nb(doc, p0_v, p1_v, p_ab)
    print "{} classified as : {}".format(doc, classify)


def text_parse(content):
    tokens = re.split(r'\W*', content)
    return [tok.lower() for tok in tokens if len(tok) > 2]


def spam_test():
    doc_list = []
    class_list = []
    full_text = []

    num_files = 25
    for i in xrange(1, num_files+1):
        words = text_parse(open('email/spam/%d.txt' % i).read())
        doc_list.append(words)
        full_text.extend(words)
        class_list.append(1)

        words = text_parse(open('email/ham/%d.txt' % i).read())
        doc_list.append(words)
        full_text.extend(words)
        class_list.append(0)

    vocab_list = create_vocab_list(doc_list)

    training_set = range(num_files*2)
    test_set = []

    for i in xrange(20):
        rand_index = int(random.uniform(0, len(training_set)))
        test_set.append(training_set[rand_index])
        del(training_set[rand_index])

    train_matrix = []
    train_classes = []
    for i in training_set:
        train_matrix.append(set_words_vec(vocab_list, doc_list[i]))
        train_classes.append(class_list[i])

    p1_v, p0_v, p_spam = train_nbayes(train_matrix, train_classes)
    error_count = 0

    for index in test_set:
        word_v = set_words_vec(vocab_list, doc_list[index])
        if classify_nb(array(word_v), p0_v, p1_v, p_spam) != class_list[index]:
            error_count += 1

    print "The error ratio is: {}".format(float(error_count)/len(test_set))


def calc_freq(vocab_list, full_text):
    freq = {}
    for token in vocab_list:
        freq[token] = full_text.count(token)

    return sorted(freq.iteritems(), key=operator.itemgetter(1), reverse=True)


def local_words(feed1, feed0):
    doc_list = []
    class_list = []
    full_text = []

    min_len = min(len(feed1['entries']), len(feed0['entries']))
    for i in xrange(min_len):
        words = text_parse(feed1['entries'][i]['summary'])
        doc_list.append(words)
        full_text.extend(words)
        class_list.append(1)

        words = text_parse(feed0['entries'][i]['summary'])
        doc_list.append(words)
        full_text.extend(words)
        class_list.append(0)

    vocab_list = create_vocab_list(doc_list)

    top30words = calc_freq(vocab_list, full_text)[:30]

    for word in top30words:
        if word[0] in vocab_list:
            vocab_list.remove(word[0])

    training_set = range(2*min_len)
    test_set = []

    for i in xrange(20):
        rand_index = random.randint(0, len(training_set))
        test_set.append(training_set[rand_index])
        del(training_set[rand_index])

    train_matrix = []
    train_classes = []
    for i in training_set:
        train_matrix.append(set_words_vec(vocab_list, doc_list[i]))
        train_classes.append(class_list[i])

    p1_v, p0_v, p_spam = train_nbayes(train_matrix, train_classes)
    error_count = 0

    for index in test_set:
        word_v = set_words_vec(vocab_list, doc_list[index])
        if classify_nb(array(word_v), p0_v, p1_v, p_spam) != class_list[index]:
            error_count += 1

    print "The error ratio is: {}".format(float(error_count)/len(test_set))

    return vocab_list, p0_v, p1_v


def get_top_words(ny, sf):
    vocabs, p_sf, p_ny = local_words(ny, sf)
    top_ny = []
    top_sf = []

    for i in xrange(len(p_sf)):
        if p_sf[i] > -6.0:
            top_sf.append((vocabs[i], p_sf[i]))
        if p_ny[i] > -6.0:
            top_ny.append((vocabs[i], p_ny[i]))

    sorted_sf = sorted(top_sf, key=lambda pair: pair[1], reverse=True)
    print "SF**"*10
    for item in sorted_sf:
        print item[0]

    sorted_ny = sorted(top_ny, key=lambda pair: pair[1], reverse=True)
    print "NY**"*10
    for item in sorted_ny:
        print item[0]





