__author__ = "Aidan O'Brien"

"""
The main module for the system, allows for running the code through a GUI, saving test outputs, loading all the required
information
"""

# Import tkinter to create the GUI
from tkinter import *
from gui import ThesisGui
import nsga

root = Tk()
root.wm_title('CubeSat Conceptual Design Generator')
root.minsize(840, 600)
root.geometry('840x600')

nsga.create_population(20)

display = ThesisGui(root)

root.mainloop()