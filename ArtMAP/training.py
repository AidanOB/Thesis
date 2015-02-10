__author__ = "Aidan O'Brien"

from artmap_utils import *


def artmap_learning(artmap_net, data, sup_data):
    """
    This function trains the artmap network on the given data
    :param artmap_net:
    :param data:
    :param sup_data:
    :return:
    """

    false_return = np.array([[False]])

    num_features, num_samples = data.shape

    if not num_features == artmap_net['num_features']:
        print('Data does not contain the same number of features as the network')
        return false_return

    if 0 >= artmap_net['vigilance'] < 1:
        print('Vigilance must fall in the [0, 1) range')
        return false_return

    if artmap_net['epoch_number'] < 1:
        print('Epochs must be a positive number')
        return false_return

    # for epoch in range(0, artmap_net['epoch_number']):
        # This variable allows us to keep track of the number of changes due to learning
    for epoch in range(0, 1):  # For testing only
        number_of_changes = 0
        for sample in range(0, num_samples):
            cur_data = data[:, sample]
            cur_super = sup_data[0, sample]
            if artmap_net['map_field'].size == 0 or np.nonzero(artmap_net['map_field'] == cur_super).size == 0:
                resized_weight, resized_map = add_new_cat(artmap_net['weights'], artmap_net['map_field'])