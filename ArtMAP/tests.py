__author__ = "Aidan O'Brien"


"""
Test set data and function to ensure that the ARTMAP module works correctly
"""

import artmap_utils
import numpy as np


def test_complement_coding():
    """
    Tests the function artmap_complement_code
    :return: True if all tests are correct, False otherwise
    """
    data_one = np.array([[0.3, 0.2, 0.4],
                         [0.6, 0.5, 0.9]])
    data_one_comp = artmap_utils.complement_code(data_one)

    data_one_comp_correct = np.array([[0.3, 0.2, 0.4],
                                      [0.7, 0.8, 0.6],
                                      [0.6, 0.5, 0.9],
                                      [0.4, 0.5, 0.1]])

    if (np.abs((data_one_comp - data_one_comp_correct)) < 1e-14).all():
        print('Complement Test one correct')
        test_one = True
    else:
        print('Complement Test one INcorrect')
        test_one = False

    data_two = np.array([[1, 1, 0, 0],
                         [1, 0, 1, 0]])
    data_two_comp = artmap_utils.complement_code(data_two)
    data_two_comp_correct = np.array([[1, 1, 0, 0],
                                      [0, 0, 1, 1],
                                      [1, 0, 1, 0],
                                      [0, 1, 0, 1]])

    if (data_two_comp == data_two_comp_correct).all():
        print('Complement Test Two correct')
        test_two = True
    else:
        print('Complement Test Two INcorrect')
        test_two = False

    test_results = np.array([test_one, test_two])

    if test_results.all():
        results = True
    else:
        results = False

    # Once more than one test is written, will check if any failed, then return True/False

    return results


def test_suite():
    """
    Tests all ArtMap code simultaneously
    :return: True for correct testing, False otherwise
    """

    complement_test = test_complement_coding()

    # utils.artmap_create_net(4, 2)

    test_add_new_cat()

    basic_test_example()

    test_results = {complement_test}

    return test_results


def basic_test_example():
    """
    This makes ARTMAP network learn the XOR function as a test of the algorithm
    :return: Number of epochs needed to learn the XOR function. Correct answer will be 2.
    """

    data = np.array([[1, 1, 0, 0],
                     [1, 0, 1, 0]])

    super_data = np.array([[0, 1, 1, 0]])

    data_comp = artmap_utils.complement_code(data)

    num_features = data.shape[1]
    num_classes = 2

    network = artmap_utils.create_net(num_features, num_classes)

    new_network = artmap_utils.artmap_learning(network, data_comp, super_data)


def test_add_new_cat():
    weight_one = np.array([[8, 1, 6],
                           [3, 5, 7],
                           [4, 9, 2]])

    map_one = np.zeros((1, 1))
    rez_weight_one, rez_map_one = artmap_utils.add_new_cat(weight_one, map_one)

    weight_empty = np.array([[]])
    map_empty = np.array([[]])
    rez_weight_empty, rez_map_empty = artmap_utils.add_new_cat(weight_empty, map_empty)




test_suite()



# utils.artmap_learning()