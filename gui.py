__author__ = "Aidan O'Brien"

"""
This has the full layout of the gui to enable easy control of the system
"""
from tkinter import *
import matplotlib
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as anima
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
        self.option_width = 20

        # Creating a main menu
        self.menu = Menu(master)
        master.config(menu=self.menu)

        self.file_menu = Menu(self.menu)
        self.menu.add_cascade(label='File', menu=self.file_menu)
        self.file_menu.add_command(label='Run', command=self.printTest)
        self.file_menu.add_command(label='Save', command=self.doNothing)
        self.file_menu.add_command(label='Save As...', command=self.doNothing)
        self.file_menu.add_command(label='Quit', command=master.quit)

        self.help_menu = Menu(self.menu)
        self.menu.add_cascade(label='Help', menu=self.help_menu)
        self.help_menu.add_command(label='About', command=self.doNothing)
        self.help_menu.add_command(label='License', command=self.doNothing)

        # Creating the frames
        toolbar = Frame(master, height=50)
        toolbar.pack(side=TOP, fill=X)

        body_frame = Frame(master)
        body_frame.pack(fill=BOTH)

        options_frame = Frame(body_frame, width=400)
        options_frame.pack(side=LEFT)

        graph_frame = Frame(body_frame)
        graph_frame.pack(fill=BOTH)

        # Toolbar Items
        self.run_photo = PhotoImage(file='./GuiFiles/run_icon_20px.gif')
        self.run_photo_grey = PhotoImage(file='./GuiFiles/run_icon_20px_grey.gif')
        self.exit_photo = PhotoImage(file='./GuiFiles/exit_icon_20px.gif')
        self.save_photo = PhotoImage(file='./GuiFiles/save_icon_20px.gif')
        self.run_button = Button(toolbar, image=self.run_photo, command=self.test_button)
        self.save_button = Button(toolbar, image=self.save_photo, command=self.doNothing)
        self.exit_button = Button(toolbar, image=self.exit_photo, command=master.quit)

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
        self.mutations_slide = Scale(options_frame, orient=HORIZONTAL, width=10, length=160,
                                     command=self.update_mutation_rate)
        self.mutations_slide.set(30)

        # NN parameters
        self.unit_label = Label(options_frame, text='CubeSat Size')
        self.unit_default = StringVar(master)
        self.unit_default.set("2U")
        self.unit_option = OptionMenu(options_frame, self.unit_default, "1U", "1.5U", "2U", "3U", "4U", "5U", "6U")
        self.unit_option.configure(width=self.option_width)

        self.size_label = Label(options_frame, text='Size Importance')
        self.size_default = StringVar(master)
        self.size_default.set("Average")
        self.size_option = OptionMenu(options_frame, self.size_default, "Very Unimportant", "Unimportant",
                                      "Less Than Average", "Average", "More Than Average", "Important",
                                      "Very Important")
        self.size_option.configure(width=self.option_width)

        self.mass_label = Label(options_frame, text='Mass Importance')
        self.mass_default = StringVar(master)
        self.mass_default.set('Average')
        self.mass_option = OptionMenu(options_frame, self.mass_default, "Very Unimportant", "Unimportant",
                                      "Less Than Average", "Average", "More Than Average", "Important",
                                      "Very Important")
        self.mass_option.configure(width=self.option_width)

        self.down_label = Label(options_frame, text='Downlink Speed')
        self.down_default = StringVar(master)
        self.down_default.set("Average")
        self.down_option = OptionMenu(options_frame, self.down_default, "Extremely Slow", "Very Slow", "Slow",
                                      "Average", "Fast", "Very Fast", "Extremely Fast")
        self.down_option.configure(width=self.option_width)

        self.up_label = Label(options_frame, text='Uplink Speed')
        self.up_default = StringVar(master)
        self.up_default.set("Average")
        self.up_option = OptionMenu(options_frame, self.up_default, "Extremely Slow", "Very Slow", "Slow", "Average",
                                    "Fast", "Very Fast", "Extremely Fast")
        self.up_option.configure(width=self.option_width)

        self.attitude_label = Label(options_frame, text="Attitude Control")
        self.attitude_default = StringVar(master)
        self.attitude_default.set("Average")
        self.attitude_option = OptionMenu(options_frame, self.attitude_default, "Extremely Lenient", "Very Lenient",
                                          "Lenient", "Average", "Precise", "Very Precise", "Extremely Precise")
        self.attitude_option.configure(width=self.option_width)

        self.altitude_label = Label(options_frame, text="Altitude Required")
        self.altitude_default = StringVar(master)
        self.altitude_default.set("LEO")
        self.altitude_option = OptionMenu(options_frame, self.altitude_default, "LEO", "Sun-Sync", "Semi-Sync",
                                          "Geo-Sync")
        self.altitude_option.configure(width=self.option_width)

        self.remote_sense_label = Label(options_frame, text="Remote Sensing")
        self.remote_default = StringVar(master)
        self.remote_default.set("If Possible")
        self.remote_option = OptionMenu(options_frame, self.remote_default, "No", "If Possible", "Yes")
        self.remote_option.configure(width=self.option_width)

        self.sense_label = Label(options_frame, text="RS Wavelengths")
        self.sense_default = StringVar(master)
        self.sense_default.set("Visual")
        self.sense_option = OptionMenu(options_frame, self.sense_default, "Ultraviolet", "Blue", "Green", "Red",
                                       "Visual", "Visual + Near IR", "Near Infrared", "Infrared", "Far Infrared",
                                       "Thermal Infrared", "Radar")
        self.sense_option.configure(width=self.option_width)

        self.sense_acc_label = Label(options_frame, text="RS Accuracy")
        self.sense_acc_default = StringVar(master)
        self.sense_acc_default.set("Average")
        self.sense_acc_option = OptionMenu(options_frame, self.sense_acc_default, "No Detail", "Vague",
                                           "Not Detailed", "Average", "Detailed", "Very Detailed", "Extremely Detailed")
        self.sense_acc_option.configure(width=self.option_width)

        # Create the Graphs to be plotted
        # Currently just placeholders for appearance
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

        self.set_positions()

    def set_positions(self):
        """
        A method to set the positions of all the widgets defined in the constructor
        """
        # Options frame
        self.set_options_positions()

        # Toolbar Frame
        self.set_toolbar_positions()

        # Status bar
        self.status_bar.pack(side=BOTTOM, fill=X)

    def set_options_positions(self):
        self.population_label.grid(row=0, column=0, sticky=E)
        self.population_entry.grid(row=0, column=1)
        self.generations_label.grid(row=1, column=0, sticky=E)
        self.generations_entry.grid(row=1, column=1)
        self.mutations_label.grid(row=2, column=0, sticky=E)
        self.mutations_slide.grid(row=2, column=1)
        self.unit_label.grid(row=3, column=0, sticky=E)
        self.unit_option.grid(row=3, column=1)
        self.mass_label.grid(row=4, column=0, sticky=E)
        self.mass_option.grid(row=4, column=1)
        self.size_label.grid(row=5, column=0, sticky=E)
        self.size_option.grid(row=5, column=1)
        self.down_label.grid(row=6, column=0, sticky=E)
        self.down_option.grid(row=6, column=1)
        self.up_label.grid(row=7, column=0, sticky=E)
        self.up_option.grid(row=7, column=1)
        self.altitude_label.grid(row=8, column=0, sticky=E)
        self.altitude_option.grid(row=8, column=1)
        self.attitude_label.grid(row=9, column=0, sticky=E)
        self.attitude_option.grid(row=9, column=1)
        self.remote_sense_label.grid(row=10, column=0, sticky=E)
        self.remote_option.grid(row=10, column=1)
        self.sense_label.grid(row=11, column=0, sticky=E)
        self.sense_option.grid(row=11, column=1)
        self.sense_acc_label.grid(row=12, column=0, sticky=E)
        self.sense_acc_option.grid(row=12, column=1)

    def set_toolbar_positions(self):
        self.run_button.grid(row=0, column=0, padx=2, pady=2)
        self.save_button.grid(row=0, column=1, padx=2, pady=2)
        self.exit_button.grid(row=0, column=2, padx=2, pady=2)

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
        An empty function to literally do nothing. Used for testing and placeholders
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