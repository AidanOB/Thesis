__author__ = "Aidan O'Brien"

"""
A module which converts the csv files into pandas data frames, for easy retrieval.
"""

import pandas as pd

structures = pd.DataFrame.from_csv(path='./Component Files/structures.csv', sep=';')

