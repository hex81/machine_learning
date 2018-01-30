#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 9/29/17 2:45 AM
# @Author  : Xin He

import matplotlib.pyplot as plt
from numpy import *


def load_data():
    data_set = []
    labels = []

    with open('testSet.txt') as fr:
        for line in fr.readlines():
            vector = map(float, line.strip().split())
            data_set.append(vector[:-1])
            labels.append(vector[-1])
    return data_set, labels


def sigmoid(z):
    return 1.0 / (1 + exp(-z))


def get_weight(data_set, labels):
    m, n = shape(data_set)
    x = ones((m, n+1))
    x[:, 1:] = data_set
    x = mat(x)
    y = mat(labels).transpose()

    alpha = 0.01
    cycles = 1000
    weights = ones((n+1, 1))

    for i in xrange(cycles):
        h = sigmoid(x*weights)
        error = h - y
        weights = weights - alpha * x.transpose() * error

    return weights


def plot_best_fit(weights):
    data_set, labels = load_data()

    m, n = shape(data_set)

    x_cord1 = []
    y_cord1 = []
    x_cord2 = []
    y_cord2 = []

    for i in xrange(m):
        if int(labels[i]) == 1:
            x_cord1.append(data_set[i][0])
            y_cord1.append(data_set[i][1])

        else:
            x_cord2.append(data_set[i][0])
            y_cord2.append(data_set[i][1])

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(x_cord1, y_cord1, s=30, c='red', marker='s')
    ax.scatter(x_cord2, y_cord2, s=30, c='green')
    x = arange(-3.0, 3.0, 0.1)
    y = (-weights[0] - weights[1]*x) / weights[2]

    ax.plot(x, y)
    plt.xlabel('X1')
    plt.ylabel('X2')
    plt.show()


def rand_grad_descent(data_set, labels):
    m, n = shape(data_set)
    x = ones((m, n + 1))
    x[:, 1:] = data_set
    x = mat(x)
    y = mat(labels).transpose()

    alpha = 0.01
    weights = ones((n + 1, 1))

    for i in xrange(m):
        h = sigmoid(x[i] * weights)
        error = h - y[i]
        weights = weights - alpha * x[i].transpose() * error

    return weights


def rand_grad_descent_e(data_set, labels, num_iter=200):
    m, n = shape(data_set)
    x = ones((m, n + 1))
    x[:, 1:] = data_set
    x = mat(x)
    y = mat(labels).transpose()

    alpha = 0.01
    weights = ones((n + 1, 1))

    for j in xrange(num_iter):
        index_list = range(m)
        for i in xrange(m):
            alpha = alpha / (1.0 + j + i) + 0.01
            index = random.choice(index_list)
            h = sigmoid(x[index] * weights)
            error = h - y[index]
            weights = weights - alpha * x[index].transpose() * error
            index_list.remove(index)

    return weights


def classify(x, weights):
    x.insert(0, 1)
    x = mat(map(float, x))
    prob = sigmoid(x * weights)
    if prob > 0.5:
        return 1.0
    else:
        return 0.0


def colic_test():
    training_set = []
    training_labels = []
    with open('horseColicTraining.txt') as f_train:
        for line in f_train.readlines():
            cur_line = line.strip().split()
            training_set.append(cur_line[:-1])
            training_labels.append(float(cur_line[-1]))

    testing_set = []
    testing_labels = []
    with open('horseColicTest.txt') as f_test:
        for line in f_test.readlines():
            cur_line = line.strip().split()
            testing_set.append(cur_line[:-1])
            testing_labels.append(float(cur_line[-1]))

    training_weights = rand_grad_descent_e(training_set, training_labels, 500)

    error_count = 0.0

    for i in xrange(len(testing_set)):
        prob = classify(testing_set[i], training_weights)
        if prob != testing_labels[i]:
            error_count += 1

    error_rate = error_count / len(testing_labels)

    print "The error rate is {}".format(error_rate)

    return error_rate


def multi_test():
    num_tests = 10
    error_sum = 0.0

    for k in xrange(num_tests):
        error_sum += colic_test()

    print "test {} times".format(num_tests)
    print "average error rate is {}".format(error_sum / float(num_tests))

