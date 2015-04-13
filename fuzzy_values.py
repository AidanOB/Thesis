__author__ = "Aidan O'Brien"

"""
Contains fuzzy values and functions to calculate fuzzy variables
"""

import numpy as np

size = {"1U": 0.,
        "1.5U": 0.167,
        "2U": 0.33,
        "3U": 0.5,
        "4U": 0.667,
        "5U": 0.834,
        "6U": 1.}
mass_imp = {"Very Unimportant": 0.,
            "Unimportant": 0.167,
            "Less Than Average": 0.33,
            "Average": 0.5,
            "More Than Average": 0.667,
            "Important": 0.834,
            "Very Important": 1.}
size_imp = {"Very Unimportant": 0.,
            "Unimportant": 0.167,
            "Less Than Average": 0.33,
            "Average": 0.5,
            "More Than Average": 0.667,
            "Important": 0.834,
            "Very Important": 1.}
down_sp = {"Extremely Slow": 0.,
           "Very Slow": 0.167,
           "Slow": 0.33,
           "Average": 0.5,
           "Fast": 0.667,
           "Very Fast": 0.834,
           "Extremely Fast": 1.0}
up_sp = {"Extremely Slow": 0.,
         "Very Slow": 0.1,
         "Slow": 0.3,
         "Average": 0.5,
         "Fast": 0.7,
         "Very Fast": 0.9,
         "Extremely Fast": 1.0}

att_ctrl = {"Extremely Lenient": 0.,
            "Very Lenient": 0.167,
            "Lenient": 0.33,
            "Average": 0.5,
            "Precise": 0.667,
            "Very Precise": 0.834,
            "Extremely Precise": 1.}
alt_req = {"LEO": 0.,
           "Sun-Sync": 0.333,
           "Semi-Sync": 0.667,
           "Geo-Sync": 1.}
remote = {"No": 0.,
          "If Possible": 0.5,
          "Yes": 1.}
rs_wave = {"Ions": 0.,
           "Electrons": 0.167,
           "Ultraviolet": 0.33,
           "Visual": 0.5,
           # "Visual + Near IR": 0.4,  # Removed due to lack of need
           # "Near Infrared": 0.5,  # Removed due to lack of need
           "Infrared": 0.667,
           # "Far Infrared": 0.7,  # Removed due to lack of need
           "Thermal Infrared": 0.9,
           # "Radar": 0.9,  # Removed because unable to find OTS components to do it
           "Radio": 1.}
rs_accuracy = {"No Detail": 0,
               "Vague": 0.167,
               "Not Detailed": 0.333,
               "Average": 0.5,
               "Detailed": 0.667,
               "Very Detailed": 0.834,
               "Extremely Detailed": 1.}
generic_vals = {"VL": 0., "L": 0.167, "ML": 0.333, "M": 0.5, "MH": 0.667, "H": 0.834, "VH": 1.}


def create_value_array(size_lang, size_imp_lang, mass_imp_lang, down_lang, up_lang, alt_lang, att_lang, remote_lang,
                          rs_wave_lang, rs_acc_lang):
    """
    This function takes the natural language values and converts them into the appropriate fuzzy logic value
    :param size_lang: Takes a value natural language input for the size dict.
    :param size_imp_lang: Natural language input for the size importance dict.
    :param mass_imp_lang: Natural language input for the mass importance dict.
    :param down_lang: Natural language input for the down bandwidth dict.
    :param up_lang: Natural language input for the uplink bandwidth dict.
    :param alt_lang: Natural language input for the altitude requirement dict.
    :param att_lang: Natural language input for the attitude control performance dict.
    :param remote_lang: Natural language input for the remote sensing requirement dict.
    :param rs_wave_lang: Natural language input for the remote sensing wavelength dict.
    :param rs_acc_lang: Natural language input for the remote sensing accuracy dict.
    :return: Single column 2D numpy array with numerical fuzzy logic values.
    """

    size_val = size[size_lang]
    size_imp_val = size_imp[size_imp_lang]
    mass_imp_val = mass_imp[mass_imp_lang]
    down_val = down_sp[down_lang]
    up_val = up_sp[up_lang]
    alt_val = alt_req[alt_lang]
    att_val = att_ctrl[att_lang]
    remote_val = remote[remote_lang]
    rs_wave_val = rs_wave[rs_wave_lang]
    rs_acc_val = rs_accuracy[rs_acc_lang]

    return np.array([[size_val, size_imp_val, mass_imp_val, down_val, up_val, alt_val, att_val, remote_val,
                      rs_wave_val, rs_acc_val]]).T