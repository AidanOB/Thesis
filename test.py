__author__ = "Aidan O'Brien"

"""
Test file for the functions involved in making systems and combining components
"""

from components import *


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
    sys_one = systems.loc[0]
    sys_one = sys_one[~sys_one.isnull()]
    parse_system(sys_one, comp_pre_built)



test_create_system()