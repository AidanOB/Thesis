__author__ = "Aidan O'Brien"

"""
Contains fuzzy values and functions to calculate fuzzy variables
"""

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
         "Very Slow": 0.167,
         "Slow": 0.33,
         "Average": 0.5,
         "Fast": 0.667,
         "Very Fast": 0.834,
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
rs_wave = {"Ultraviolet": 0.,
           "Blue": 0.1,
           "Green": 0.2,
           "Red": 0.3,
           "Visual": 0.4,
           "Visual + Near IR": 0.5,
           "Near Infrared": 0.6,
           "Infrared": 0.7,
           "Far Infrared": 0.8,
           "Thermal Infrared": 0.9,
           "Radar": 1.}
rs_accuracy = {"No Detail": 0,
               "Vague": 0.167,
               "Not Detailed": 0.333,
               "Average": 0.5,
               "Detailed": 0.667,
               "Very Detailed": 0.834,
               "Extremely Detailed": 1.}
