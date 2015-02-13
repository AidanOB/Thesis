__author__ = "Aidan O'Brien"

"""
A module which converts the csv files into pandas data frames, for easy retrieval.
"""

import pandas as pd
import numpy as np
from fuzzy_values import *

structures = pd.DataFrame.from_csv(path='./Component Files/structures.csv', sep=';', encoding='iso-8859-1')

components = pd.DataFrame.from_csv(path='./Component Files/components.csv', sep=';', encoding='iso-8859-1')

systems = pd.DataFrame.from_csv(path='./Component Files/systems.csv', sep=';', encoding='iso-8859-1')

comp_hidden = pd.DataFrame.from_csv(path='./Component Files/components_hidden.csv', sep=';', encoding='iso-8859-1')

comp_pre_built = pd.concat([comp_hidden, components], ignore_index=True)


def create_system(sys_structure):
    """
    This function creates a system from the dict structure given. It combines the components listed and then returns
      the product specifications.
    :param sys_structure: A dict that lists all the components that are a part of the system
    :return: A dictionary the lists the product specifications as generated
    """
    pass


def parse_system(system, comps):
    """
    This function parses the data frame row for an individual system, converting it into a dictionary for creating the
     product specifications
    :param system: A row from a Pandas Data Frame.
    :param comps: Defines which components database to search
    :return: A dictionary containing all the components for the system
    """

    # Load the structure from the data frame given
    print(system['Structure'])
    struct = structures.loc[structures['Name'].isin([system['Structure']])]
    internal_vol = struct.X[0] * struct.Y[0] * struct.Z[0]

    # Extract the fuzzy values for the system and place them into a numpy array of features for FAM algorithm
    size_val = size[system['Size']]
    size_imp_val = size_imp[system['Size Imp']]
    mass_imp_val = mass_imp[system['Mass Imp']]
    down_val = down_sp[system['Down Sp']]
    up_val = up_sp[system['Up Sp']]
    alt_val = alt_req[system['Alt Req']]
    att_val = att_ctrl[system['Att Ctrl']]
    remote_val = remote[system['Remote']]
    rs_wave_val = rs_wave[system['RS Wave']]
    rs_acc_val = rs_accuracy[system['RS Accuracy']]

    cust_reqs = np.array([size_val, size_imp_val, mass_imp_val, down_val, up_val, alt_val, att_val, remote_val,
                          rs_wave_val, rs_acc_val])

    # Todo calculate all components in the system and provide system outputs that can be converted into metrics


