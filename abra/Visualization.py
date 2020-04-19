import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
# from . import data

class GoodBad(tk.Tk):

    def __init__(self, data, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.data = data

        self.frames = {}

        frame = Pupil_Vis(container, self)

        self.frames[Pupil_Vis] = frame

        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Pupil_Vis)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


class Pupil_Vis(tk.Frame):

    def __init__(self, parent, controller):
        self.data = controller.data
        self.pup_size = []
        self.timestmp = []
        self.index = 0
        #0 = bad and 1 = good
        self.curr_quailty = 0
        self.pupil_trials = self.data.get_values()
        self.timestamp_trials = self.data.get_timestamps()
        self.quality_list = np.zeros(len(self.pupil_trials))

        #initalize timestamps in milliseconds(0-end)
        for t in range(len(self.timestamp_trials)):
            self.timestamp_trials[t] -= self.timestamp_trials[0]

        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Pupil Size")
        label.pack(pady=10,padx=10)

        # self.next_graph

        good_button = ttk.Button(self, text="Good",
                            command=lambda: self.good_button_function())
        good_button.pack()

        bad_button = ttk.Button(self, text="Bad",
                            command=lambda: self.bad_button_function())
        bad_button.pack()

        next_button = ttk.Button(self, text="Next",
                            command=lambda: self.next_graph())
        next_button.pack()

        previous_button = ttk.Button(self, text="Previous",
                            command=lambda: self.previous_graph())
        previous_button.pack()


        self.f = Figure(figsize=(5,5), dpi=100)
        self.a = self.f.add_subplot(111)
        self.a.plot(self.timestamp_trials[index],self.pupil_trials[index])

        self.canvas = FigureCanvasTkAgg(self.f, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


    def next_graph(self):
        # get pupil size data from index
        self.a.clear()
        self.canvas.get_tk_widget().destroy()
        self.index += 1

        if(self.index >= len(self.pupil_trials)):
            messagebox.showinfo('End of List')
            self.index -= 1
            pass
        self.f = Figure(figsize=(5,5), dpi=100)
        self.a = self.f.add_subplot(111)
        self.a.plot(self.timestamp_trials[index],self.pupil_trials[index])

        self.canvas = FigureCanvasTkAgg(self.f, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def previous_graph(self):
        # get pupil size data from index
        self.a.clear()
        self.canvas.get_tk_widget().destroy()
        self.index -= 1
        if(self.index < 0):
            messagebox.showinfo('Out of Index','You are at the begining of the List')
            self.index = 0
            pass
        self.f = Figure(figsize=(5,5), dpi=100)
        self.a = self.f.add_subplot(111)
        self.a.plot(self.timestamp_trials[index],self.pupil_trials[index])

        self.canvas = FigureCanvasTkAgg(self.f, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


    def good_button_function(self):
        self.quality_list[index] = 1

    def bad_button_function(self):
        self.quality_list[index] = 0


default_obj = data.read("abra/test/asc/1211NE1.asc")
sess = default_obj.create_session()

app = GoodBad(sess)
# app.read_data(data)
app.mainloop()
