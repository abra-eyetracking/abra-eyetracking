import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np
import time

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog as fd

from . import data


#creates initial window for visualization
class Visualization(tk.Tk):
    '''
    Creates a Visualization Object To Identify Good and Bad Trials
    By Visualizing Pupil Size Across trial_stamp

    Parameter Input:
    data: Sessions data object
        > will separate pupil size and timestamps to plot

    Visualization will a GUI that will show the plot of pupil size
    across trials. Good, Bad, Next and Previous buttons will be shown
    with the graph.

    Good button: will classify that the trial is good(1)

    Bad button: will classify that the trial is bad(0)

    Next: will move to the next trial
        - Will warn you when you are at the last trial
        - Window will open asking if you want to quit or return to
          the graphs

    Previous button: will move to the previous trial
        - Will warn you when are on the first trial and you press
          previous.

    Return:

    trial_quality: a list of all the quality classification for
                   all trials
    '''



    def __init__(self, data, quality_list, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.data = data

        #data has trials values of pupil size and timestamps
        self.pup_size = []
        self.timestmp = []
        self.index = 0

        #0 = bad and 1 = good
        self.curr_quailty = 0
        self.pupil_trials = self.data.get_pupil()
        self.movement_trials = self.data.get_movement()
        self.timestamp_trials = self.data.get_timestamps()
        if quality_list:
            file = fd.askopenfilename()
            self.quality_list = np.loadtxt(file)
        else:
            self.quality_list = np.ones(len(self.pupil_trials)) # change to all 1

        #initalize timestamps in milliseconds(0-end)
        self.tick = (1000/self.data.sample_rate)
        print(self.pupil_trials.shape)
        for t in range(len(self.pupil_trials)):
            # print(t.shape)
            for ind in range(len(self.pupil_trials[t])):
                self.timestamp_trials[t][ind] = self.tick * ind
            # self.timestamp_trials[t] -= self.timestamp_trials[t][0]

        good_button = ttk.Button(self,
                            text="Good",
                            command=lambda: self.good_button_function())
        good_button.pack(side = tk.TOP)

        bad_button = ttk.Button(self,
                            text="Bad",
                            command=lambda: self.bad_button_function())
        bad_button.pack(side = tk.TOP)

        next_button = ttk.Button(self,
                            text="Next",
                            command=lambda: self.next_graph())
        next_button.pack(side = tk.TOP)

        previous_button = ttk.Button(self,
                            text="Previous",
                            command=lambda: self.previous_graph())
        previous_button.pack(side = tk.TOP)

        save_button = ttk.Button(self,
                                text = "Save",
                                command = lambda: self.save())
        save_button.pack(side = tk.TOP)


        self.my_text = ttk.Label(self,
         text= f"Graph: {self.index +1}     Quality: {self.quality_list[self.index]}")
        self.my_text.pack(side = tk.TOP)

        self.f = Figure(figsize=(5,5), dpi=100)
        self.a = self.f.add_subplot(211)
        self.a.plot(self.timestamp_trials[self.index],
                    self.pupil_trials[self.index])
        self.a.set_title('Pupil Size Trial {}'.format(str(self.index+1)))
        self.a.set_xlabel('Time (ms)')
        self.a.set_ylabel('Pupil Size')

        self.a = self.f.add_subplot(212)
        self.a.plot(self.timestamp_trials[self.index], self.movement_trials[0][self.index], label = 'x-axis movement')
        self.a.plot(self.timestamp_trials[self.index], self.movement_trials[1][self.index], label = 'y-axis movement')
        self.a.legend(loc='upper center', bbox_to_anchor=(0.5, 1.3), fontsize = 'small', ncol = 2)
        self.a.set_title('X and Y Axis Movement Trial {}'.format(str(self.index+1)), pad = 30)
        self.a.set_xlabel('Time (ms)')
        self.a.set_ylabel('Axis')
        self.f.tight_layout(pad = 3)

        self.canvas = FigureCanvasTkAgg(self.f, self)
        self.canvas.draw()
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.BOTTOM,
                                   fill=tk.BOTH,
                                   expand=True)
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM,
                                         fill=tk.BOTH,
                                         expand=True)



    #gets next graph by getting adding 1 to the current position (index)
    def next_graph(self):
        # get pupil size data from index

        self.a.clear()
        self.canvas.get_tk_widget().destroy()


        if(self.index >= len(self.pupil_trials)-1):
            finished = messagebox.askquestion('Finished',
                        'This is the last graph\nDo you want to save and exit?')

            if finished == 'yes':
                file = fd.asksaveasfile(mode = 'w', defaultextension = '.txt')
                np.savetxt(file, self.quality_list)
                self.quit()

            self.index -= 1
            self.next_graph()

        else:
            self.index += 1
            self.f = Figure(figsize=(5,5), dpi=100)
            self.a = self.f.add_subplot(211)
            self.a.plot(self.timestamp_trials[self.index],
                        self.pupil_trials[self.index])
            self.a.set_title('Pupil Size Trial {}'.format(str(self.index+1)))
            self.a.set_xlabel('Time (ms)')
            self.a.set_ylabel('Pupil Size')

            self.a = self.f.add_subplot(212)
            self.a.plot(self.timestamp_trials[self.index], self.movement_trials[0][self.index], label = 'x-axis movement')
            self.a.plot(self.timestamp_trials[self.index], self.movement_trials[1][self.index], label = 'y-axis movement')
            self.a.legend(loc='upper center', bbox_to_anchor=(0.5, 1.3), fontsize = 'small', ncol = 2)
            self.a.set_title('X and Y Axis Movement Trial {}'.format(str(self.index+1)), pad = 30)
            self.a.set_xlabel('Time (ms)')
            self.a.set_ylabel('Axis')
            self.f.tight_layout(pad = 3)

            self.canvas = FigureCanvasTkAgg(self.f, self)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(side=tk.BOTTOM,
                                             fill=tk.BOTH,
                                             expand=True)

            self.toolbar.update()
            self.canvas._tkcanvas.pack(side=tk.BOTTOM,
                                       fill=tk.BOTH,
                                       expand=True)
            self.my_text.pack_forget()
            self.my_text = ttk.Label(self,
                                    text= f"Graph: {self.index +1}     {self.quality_list[self.index]}")
            self.my_text.pack(side = tk.TOP)

    #gets previous graph by subtracting 1 to the current position (index)
    def previous_graph(self):
        # get pupil size data from index
        self.a.clear()
        self.canvas.get_tk_widget().destroy()
        self.index -= 1
        if(self.index < 0):
            messagebox.showinfo('Out of Index',
                            'You are at the begining of the List')
            self.index = 0
            pass
        self.f = Figure(figsize=(5,5), dpi=100)
        self.a = self.f.add_subplot(211)
        self.a.plot(self.timestamp_trials[self.index],
                    self.pupil_trials[self.index])
        self.a.set_title('Pupil Size Trial {}'.format(str(self.index+1)))
        self.a.set_xlabel('Time (ms)')
        self.a.set_ylabel('Pupil Size')

        self.a = self.f.add_subplot(212)
        self.a.plot(self.timestamp_trials[self.index], self.movement_trials[0][self.index], label = 'x-axis movement')
        self.a.plot(self.timestamp_trials[self.index], self.movement_trials[1][self.index], label = 'y-axis movement')
        self.a.legend(loc='upper center', bbox_to_anchor=(0.5, 1.3), fontsize = 'small', ncol = 2)
        self.a.set_title('X and Y Axis Movement Trial {}'.format(str(self.index+1)), pad = 30)
        self.a.set_xlabel('Time (ms)')
        self.a.set_ylabel('Axis')
        self.f.tight_layout(pad = 3)

        self.canvas = FigureCanvasTkAgg(self.f, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM,
                                         fill=tk.BOTH,
                                         expand=True)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.BOTTOM,
                                   fill=tk.BOTH,
                                   expand=True)

        self.my_text.pack_forget()
        self.my_text = ttk.Label(self,
                                 text= f"Graph: {self.index +1}     {self.quality_list[self.index]}")
        self.my_text.pack(side = tk.TOP)

    #if current graph is good, change value to 1
    def good_button_function(self):
        self.quality_list[self.index] = 1

        self.my_text.pack_forget()
        self.my_text = ttk.Label(self,
                                 text= f"Graph: {self.index +1}     {self.quality_list[self.index]}")
        self.my_text.pack(side = tk.TOP)

    #if current grpah is bad, change value to 0
    def bad_button_function(self):
        self.quality_list[self.index] = 0

        self.my_text.pack_forget()
        self.my_text = ttk.Label(self,
                                 text= f"Graph: {self.index +1}     {self.quality_list[self.index]}")
        self.my_text.pack(side = tk.TOP)

    def save(self):
        save_txt = messagebox.askquestion('save',
                                          'Do you want to save and exit?')
        if save_txt == 'yes':
            file = fd.asksaveasfile(mode = 'w', defaultextension = '.txt')
            np.savetxt(file, self.quality_list)
            file.close()
            # time.sleep(1)
            self.quit()

def run_app(filename, mode="d", start_msg=r"TRIAL \d{1,2} START",
            end_msg=r"TRIAL \d{1,2} END", autoepoch=False,
            preprocess = True, buffer=50,
            interpolate='linear', inplace=False):
    Data = data.read(filename, mode, start_msg, end_msg, autoepoch)
    # if preprocess:
        # Data = data.pupil_size_remove_eye_blinks(Data, buffer, interpolate, inplace)

    sess = Data.create_session()
    app = Visualization(sess)
    app.mainloop()
    return app

    '''
    argparse
    '''
