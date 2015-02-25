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

    for epoch in range(0, artmap_net['epoch_number']):
        # This variable allows us to keep track of the number of changes due to learning

        number_of_changes = 0
        for sample in range(0, num_samples):
            cur_data = data[:, sample]
            cur_super = sup_data[0, sample]

            cur_super_match = 1
            if artmap_net['map_field'].size != 0:
                for i in range(0, len(artmap_net['map_field'][0])):
                    if artmap_net['map_field'][0, i] == cur_super:
                        cur_super_match = 0

            if artmap_net['map_field'].size == 0 or cur_super_match:
                resized_weight, resized_map = add_new_cat(artmap_net['weights'], artmap_net['map_field'])
                resized_weight, change = update_weights(cur_data, resized_weight, resized_map.shape[1],
                                                        artmap_net['learning_rate'])
                artmap_net['weights'] = resized_weight
                artmap_net['num_categories'] += 1
                resized_map[0, -1] = cur_super
                artmap_net['map_field'] = resized_map
                number_of_changes += 1
                continue

            else:
                # Activating the categories for this sample
                category_activation = category_activate(cur_data, artmap_net['weights'], artmap_net['bias'])

                # Ranking of the activations from lowest to highest
                sorted_activations, sorted_categories = sort_like_matlab(-category_activation)

                # Go through each category in the sorted list, looking for the best match
                vigilance = artmap_net['vigilance']
                resonance = 0
                num_sorted_categories = len(sorted_categories)
                curr_sorted_index = 1
                while not resonance:
                    curr_category = sorted_categories[curr_sorted_index - 1]
                    curr_weight_vector = artmap_net['weights'][:, curr_category]

                    match = calculate_match(cur_data, curr_weight_vector)

                    # Check to see if the match is less than the vigilance
                    if match < vigilance:
                        if curr_sorted_index == num_sorted_categories:
                            if curr_sorted_index == artmap_net['max_num_categories'] + 1:
                                print('WARNING: Maximum number of categories has been reached')
                                resonance = 1
                            else:
                                resized_weight, resized_map = add_new_cat(artmap_net['weights'],
                                                                          artmap_net['map_field'])
                                resized_weight, change = update_weights(cur_data, resized_weight, curr_sorted_index + 1,
                                                                        artmap_net['learning_rate'])
                                artmap_net['weights'] = resized_weight
                                artmap_net['num_categories'] += 1
                                resized_map[0, curr_sorted_index] = cur_super
                                artmap_net['map_field'] = resized_map
                                number_of_changes += 1
                                resonance = 1

                        else:
                            curr_sorted_index += 1
                    else:
                        if artmap_net['map_field'][0, curr_category] == cur_super:
                            artmap_net['weights'], change = update_weights(cur_data, artmap_net['weights'],
                                                                           curr_category + 1, artmap_net['learning_rate'])
                            if change == 1:
                                number_of_changes += 1

                            resonance = 1

                        else:
                            vigilance = match + 0.000001
                            if curr_sorted_index == num_sorted_categories:
                                if curr_sorted_index == artmap_net['max_num_categories']:
                                    print('WARNING: Maximum number of categories reached')
                                    resonance = 1
                                else:
                                    resized_weight, resized_map = add_new_cat(artmap_net['weights'],
                                                                              artmap_net['map_field'])
                                    resized_weight, change = update_weights(cur_data, resized_weight,
                                                                            curr_sorted_index + 1,
                                                                            artmap_net['learning_rate'])
                                    artmap_net['weights'] = resized_weight
                                    artmap_net['num_categories'] += 1
                                    resized_map[0, curr_sorted_index] = cur_super
                                    artmap_net['map_field'] = resized_map

                                    number_of_changes += 1

                                    resonance = 1
                            else:
                                curr_sorted_index += 1
                                resonance = 0

        if number_of_changes == 0:
            break

    print('Number of epochs required was ' + str(epoch + 1))

    return artmap_net


def train_network(data, supervisor):
    """
    This function abstracts out the learning process for the Fuzzy ARTMAP algorithm.
    :param data: The data of the training set
    :param supervisor: The supervisor data, to train against
    :return: new_network, the trained ARTMAP network utilised in classification and measurement of new data
    """

    data_comp = complement_code(data)

    num_features = data.shape[1]
    num_classes = 2

    network = create_net(num_features, num_classes)

    new_network = artmap_learning(network, data_comp, supervisor)

    return new_network