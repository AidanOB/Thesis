__author__ = "Aidan O'Brien"

"""
This module contains generalised functions for use within ARTMAP algorithms
"""

import numpy as np


def complement_code(data):
    """
    This function complement codes the input data. Where the given data is x, the complement is x - 1.
    For example: data ->    0.3 0.2 0.4
                            0.6 0.5 0.9
                 return ->  0.3 0.2 0.4
                            0.7 0.8 0.6
                            0.6 0.5 0.9
                            0.4 0.5 0.1
    :param data: This is a numpy array of num_features by num_samples that holds the data to be complement coded
    :return: The complement coded data as a matrix of size 2*num_features by num_samples
    """

    num_features, num_samples = data.shape
    complement_data = np.ones((2*num_features, num_samples))

    for i in range(num_samples):
        count = 0
        for j in range(0, 2*num_features, 2):
            complement_data[j, i] = data[count, i]
            complement_data[j + 1, i] = 1 - data[count, i]
            count += 1

    return complement_data


def create_net(num_features, num_classes, vigilance=0.75, bias=1.0e-6, max_categories=100, start_categories=0,
                      epochs=100, learning_rate=1):
    """
    This function creates a neural network for the artmap algorithm with the given number of features and classes.
    :param num_features: Number of features in the data
    :param num_classes: Number of classes for the supervisory signal
    The following parameters are set to defaults, but can be changed manually
    :param vigilance: Set to 0.75
    :param bias: Set to 0.000001
    :param max_categories: Set to 100
    :param start_categories: Set to 0
    :param epochs: Defaults to 100
    :param learning_rate: Set to 1, aka Fast Learning
    :return:
    """
    num_features = np.round(num_features)
    num_classes = np.round(num_classes)

    if num_features < 1:
        print('Number of feaures must be a positive integer.')
        return False

    if num_classes < 1:
        print('Number of classes must be a positive number greater than 1.')
        return False

    # Initialise and create the weight matrix and map field
    weight_matrix = np.ones((num_features, 0))
    map_field = np.zeros((0, 0))

    # Create a dictionary to contain all the data for the network
    network = {'num_features': num_features, 'num_categories': start_categories, 'max_num_categories': max_categories,
               'num_classes': num_classes, 'weights': weight_matrix, 'map_field': map_field, 'vigilance': vigilance,
               'bias': bias, 'epoch_number': epochs, 'learning_rate': learning_rate}

    return network


def add_new_cat(weight, map_field):
    """
    This function returns updated weight matrices and map_fields, identical to the previous version, except extended
    :param weight: A matrix that contains the current weights
    :param map_field: The map field, allowed to be empty
    :return: extended weight and map_field matrices
    """
    num_features, num_categories = weight.shape
    new_cat = np.ones((num_features, 1))
    resized_weight = np.concatenate((weight, new_cat), axis=1)
    if not map_field.size == 0:
        resized_map = np.concatenate((map_field, np.array([[0]])), axis=1)
    else:
        resized_map = np.array([[0]])
    return resized_weight, resized_map


def update_weights(inputs, weights, category_num, learn_rate):
    """
    This function returns a new weight matrix which has learned the input for the category and whether or not it was
    changed
    :param inputs: A vector
    :param weights:
    :param category_num:
    :param learn_rate:
    :return:
    """



