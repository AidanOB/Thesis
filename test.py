__author__ = "Aidan O'Brien"

"""
Test file for the functions involved in making systems and combining components
"""

from components import *
from training import *


def test_components_load():
    """
    This loads the components file and runs analysis on it
    :return: True if no errors found
    """


def test_create_system():
    """
    Tests the create_system function in the components module. Works by first parsing a pre-created system from the
    database, then creating the system.
    :return: Returns True if all systems test correctly
    """
    # sys_one = systems.loc[0]
    # sys_one = sys_one[~sys_one.isnull()]
    # sys_one_mets, sys_one_cr = parse_system(sys_one, comp_pre_built)
    # # print(sys_one_mets)
    # sys_two = systems.loc[1]
    # sys_two = sys_two[~sys_two.isnull()]
    # sys_two_mets, sys_two_cr = parse_system(sys_two, comp_pre_built)
    # print(sys_two_mets)
    # print(np.concatenate((sys_one_mets, sys_two_mets), 1))
    # print(np.concatenate((sys_one_cr, sys_two_cr), 1))
    sys_crs = np.zeros((0, 0))
    sys_mets = np.zeros((0, 0))

    for sys_row in range(5):
        # print('System number:' + str(sys_row))

        sys = systems.loc[sys_row]
        sys = sys[~sys.isnull()]
        temp_sys_mets, temp_sys_crs = parse_system(sys, comp_pre_built)
        if sys_crs.shape == (0, 0):
            sys_crs = temp_sys_crs
        else:
            sys_crs = np.concatenate((sys_crs, temp_sys_crs), 1)
        if sys_mets.shape == (0, 0):
            sys_mets = temp_sys_mets
        else:
            sys_mets = np.concatenate((sys_mets, temp_sys_mets), 1)
    print(sys_mets)
    # print(systems)
    # print(sys_crs[[6, 9], :])

    # test_net = train_network(sys_crs[[6, 9], :], sys_mets)

    # print(test_net)






test_create_system()