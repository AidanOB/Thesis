__author__ = "Aidan O'Brien"

"""
This has the full layout of the gui to enable easy control of the system
"""
from tkinter import *
import tkinter as tk
import matplotlib
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
style.use("ggplot")

import time


class ThesisGui:
    """
    This creates the gui, based around a three frame layout
    """
    def __init__(self, master):
        # Create default values
        self.generations = 5000
        self.population_size = 1000
        self.mutation_rate = 0.3

        # Creating a main menu
        self.menu = Menu(master)
        master.config(menu=self.menu)

        self.sub_menu = Menu(self.menu)
        self.menu.add_cascade(label='File', menu=self.sub_menu)
        self.sub_menu.add_command(label='Run', command=self.printTest)
        self.sub_menu.add_command(label='Save', command=self.doNothing)
        self.sub_menu.add_command(label='Save As...', command=self.doNothing)
        self.sub_menu.add_command(label='Quit', command=master.quit)

        # Creating the frames
        toolbar = Frame(master, height=50)
        toolbar.pack(side=TOP, fill=X)

        body_frame = Frame(master)
        body_frame.pack(fill=BOTH)

        options_frame = Frame(body_frame)
        options_frame.pack(side=LEFT)

        graph_frame = Frame(body_frame)
        graph_frame.pack(fill=BOTH)

        # Toolbar Items
        self.run_photo = PhotoImage(file='./GuiFiles/run_icon_20px.gif')
        self.run_photo_grey = PhotoImage(file='./GuiFiles/run_icon_20px_grey.gif')
        self.exit_photo = PhotoImage(file='./GuiFiles/exit_icon_20px.gif')
        self.save_photo = PhotoImage(file='./GuiFiles/save_icon_20px.gif')
        self.run_button = Button(toolbar, image=self.run_photo, command=self.test_button)
        self.run_button.grid(row=0, column=0, padx=2, pady=2)
        self.save_button = Button(toolbar, image=self.save_photo, command=self.doNothing)
        self.save_button.grid(row=0, column=1, padx=2, pady=2)
        self.exit_button = Button(toolbar, image=self.exit_photo, command=master.quit)
        self.exit_button.grid(row=0, column=2, padx=2, pady=2)

        # Items in the options frame
        self.population_label = Label(options_frame, text='Population Size')
        self.population_entry = Spinbox(options_frame, from_=0, to=100000, increment=100, width=10,
                                        command=self.update_population_size)
        self.population_entry.delete(0, 'end')
        self.population_entry.insert(0, self.population_size)

        self.generations_label = Label(options_frame, text='Generations')
        self.generations_entry = Spinbox(options_frame, from_=0, to=20000, increment=100, width=10,
                                         command=self.update_generations)
        self.generations_entry.delete(0, 'end')
        self.generations_entry.insert(0, self.generations)

        self.mutations_label = Label(options_frame, text='Mutation Rate')
        self.mutations_slide = Scale(options_frame, orient=HORIZONTAL, width=10, command=self.update_mutation_rate)
        self.mutations_slide.set(30)

        self.population_label.grid(row=0, column=0, sticky=E)
        self.population_entry.grid(row=0, column=1)
        self.generations_label.grid(row=1, column=0, sticky=E)
        self.generations_entry.grid(row=1, column=1)
        self.mutations_label.grid(row=2, column=0, sticky=E)
        self.mutations_slide.grid(row=2, column=1)

        # Create the Graphs to be plotted
        self.fig = Figure(figsize=(5, 5), dpi=100)
        self.fig.set_facecolor('white')
        self.sub_plot_one = self.fig.add_subplot(211)
        self.sub_plot_one.plot([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [3, 4, 6, 1, 5, 7, 8, 1, 7, 9])
        self.sub_plot_two = self.fig.add_subplot(212)
        self.sub_plot_two.plot([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [8, 3, 9, 2, 0, 2, 9, 1, 6, 7])
        self.canvas = FigureCanvasTkAgg(self.fig, graph_frame)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(fill=BOTH, expand=True)

        # Creating the status bar
        self.status_message = StringVar()
        self.status_bar = Label(master, textvariable=self.status_message, bd=1, relief=SUNKEN, anchor=W)
        self.status_bar.pack(side=BOTTOM, fill=X)

    def update_generations(self):
        self.generations = int(self.generations_entry.get())
        self.set_status_message()

    def update_population_size(self):
        self.population_size = int(self.population_entry.get())
        self.set_status_message()

    def update_mutation_rate(self, mut_rate):
        self.mutation_rate = float(mut_rate) / 100
        self.set_status_message()

    def set_status_message(self):
        self.status_message.set('Population: ' + '{message: <16}'.format(message=str(self.population_size)) +
                                'Generations Selected: ' + '{message: <16}'.format(message=str(self.generations)) +
                                'Mutation Rate: ' + str(self.mutation_rate))

    def doNothing(self):
        """
        An empty function to literally do nothing
        :return:
        """
        pass

    def printTest(self):
        print('Test correct')

    def test_button(self):
        print('Button Test')
        self.run_button['state'] = 'disabled'
        time.sleep(3)
        self.run_button['state'] = 'normal'