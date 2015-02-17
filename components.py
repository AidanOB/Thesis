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
    :return: Two arrays, the first are the customer requirements features returned as fuzzy logic values, the second is
    the product specification values. These will not be normalised.
    """

    # Load the structure from the data frame given
    # print(system)
    struct = structures.loc[structures['Name'].isin([system['Structure']])]
    internal_slots = struct['Internal Slots'].values
    external_slots = struct['External Slots'].values
    internal_vol = struct.X[0] * struct.Y[0] * struct.Z[0]
    total_vol = 0

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

    comp_totals = system.to_dict()
    comp_list = list()
    for heading in comp_totals:
        if "Comp" in heading:
            comp_list.append(heading)

    for part in comp_list:
        idx = comps['Name'] == system[part]
        component = comps.loc[idx]
        # print(component)
        parse_component(comps.loc[idx])

    # Todo calculate all components in the system and provide system outputs that can be converted into metrics


def parse_component(component):
    """
    This function calculates the various dimensions and metrics that can be utilised for the features, then returns them
    for summation in the parse system function
    :param component: The single line dataframe or series to be parsed
    :return:
    """
    # Volume of the component in m^3
    volume = (component.X * component.Y * component.Z).values[0]

    # How many slots the component takes up
    internal_slots = component['Internal Slots'].values[0]

    if not component['External Slots'].values == 0:
        external = True
        external_slots = component['External Slots'].values[0]
    else:
        external = False
        external_slots = 0

    min_temp = component['Min Temp'].values[0]
    max_temp = component['Max Temp'].values[0]

    mass = component['Mass'].values[0]
    max_voltage = component['Voltage'].values[0]
    nom_power = component['Nom Power'].values[0]
    max_power = component['Power (W)'].values[0] - nom_power  # This returns the difference when activated
    discharge_time = component['Discharge Time (Wh)'].values[0]
    pixel_resolution = component[''].values[0]
    wavelength_resolution = component[''].values[0]
    min_wavelength = component[''].values[0]
    max_wavelength = component[''].values[0]
    field_of_view = component[''].values[0]
    rx_min = component[''].values[0]
    rx_max = component[''].values[0]
    tx_min = component[''].values[0]
    tx_max = component[''].values[0]
    duplex = component[''].values[0] + 1
    br_down = component[''].values[0]
    br_up = component[''].values[0]
    data = component[''].values[0]
    code = component[''].values[0]
    ram = component[''].values[0]
    att_know = component[''].values[0]
    att_mom = component[''].values[0]
    max_prop = component[''].values[0]
    att_type = component[''].values[0]
    axis = component[''].values[0]
    ctrl_area = component[''].values[0]
    disposal = component[''].values[0]
    int_comms = component[''].values[0]
    comm_conn = component[''].values[0]
    price = component[''].values[0]

    print(volume, mass, internal_slots, external_slots, min_temp, max_temp)

    # Todo Put column headings into the components being pulled.
    # Todo Create numpy array of component variables
    # Todo create matrix from arrays then sum each feature on the correct axis
    # Todo This will create the correct feature set
    # Other features will be made from summation of available slots/connects vs used
