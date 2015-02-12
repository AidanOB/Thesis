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
    :param inputs: A vector which has the length of the number of features in the network. It contains the signal input
        into the network
    :param weights: A matrix of size num_features-by-num_categories which holds the current weights of the network
    :param category_num: The current category for the encoding of the current input range [0, num_categories)
    :param learn_rate: The learning rate at which the network learns new inputs. [0, 1]
    :return: updated_weights, changed. updated_weights is a matrix of num_features-by-num_categories containing the
        updated weights. changed is a binary number which confers whether or not the weight matrix was changed
    """

    num_features, num_categories = weights.shape

    assert len(inputs) == num_features, 'The length of the inputs and the rows of the weights do not match'
    assert (category_num >= 1) or (category_num < num_categories), \
        'The category must be in the range [1, num_categories]'

    changed = 0
    for i in range(num_features):
        if inputs[i] < weights[i, category_num - 1]:
            weights[i, category_num - 1] = learn_rate * inputs[i] + (1 - learn_rate) * weights[i, category_num - 1]
            changed = 1
    return weights, changed


def category_activate(inputs, weights, bias):
    """
    Activates categories in an ART/ARTMAP network
    :param inputs: A vector of size num_features that contains the signal input into the network
    :param weights: A matrix of size num_features-by-num_categories which holds the weights of the network
    :param bias: A constant utilised to differentiate between very similar category activation numbers
    :return: A vector of size num_categories that holds the activation value for each category
    """
    num_features, num_categories = weights.shape
    category_activated = np.ones((1, num_categories))
    # print(weights)
    for j in range(num_categories):
        match_vector = np.min(np.array([inputs, weights[:, j]]).T, axis=1)
        weight_length = np.sum(weights[:, j])
        category_activated[0, j] = np.sum(match_vector) / (bias + weight_length)

    return category_activated


def sort_like_matlab(data):
    """
    This function performs a sort and returns the original indices as the recond return value
    :param data: A numpy array to be sorted in ascending order
    :return: sorted_data, data_indices
    """
    sorted_data = np.sort(data)
    data_indices = np.argsort(data)[0]
    return sorted_data, data_indices


def calculate_match(data, weight_vector):
    """
    Calculates a similarity value that represents the match between the given data and the given category weight
    :param data: A vector of size num_features that contains the signal input
    :param weight_vector: A vector of size num_features that holds the weights of the network for a given category
    The length of the data must match the length of the weight vector.
    :return: The match value of the similarity between the input and the current category
    """

    num_features = len(data)
    assert (num_features == len(weight_vector)), 'The data and weight_vector lengths do not match.'
    # print(np.array([data, weight_vector]).T)
    match_vector = np.min(np.array([data, weight_vector]).T, axis=1)
    # print(match_vector)
    data_length = np.sum(data)
    # print(data_length)
    if data_length == 0:
        match = 0
    else:
        match = np.sum(match_vector) / data_length

    return match


def classify(artmap_net, data):
    """
    Uses the ARTMAP network to classify the given data. It utilises the network to classify the given input with the
    specified vigilance parameter (given by the network). Each sample is given is presented to the network, which then
    classifies it.
    :param artmap_net: This is a trained artmap network. Use create_network() and training.artmap_learning() to create
    and train the network respectively
    :param data: The classification data to be presented to the network. It's a matrix of size num_features-by-
     num_samples.
    :return: A vector of size num_samples that contains the class in which the ARTMAP network placed each sample. If a
    sample is unable to be classified,
    """

    num_features, num_samples = data.shape

    assert num_features == artmap_net['num_features'], \
        'The data does not contain the same number of features as the network'
    print()
    assert not (artmap_net['vigilance'] <= 0) or not (artmap_net['vigilance'] > 1), \
        'The vigilance must be in the range (0, 1]'

    classification = np.zeros((1, num_samples))

    for sample in range(num_samples):
        cur_data = data[:, sample]

