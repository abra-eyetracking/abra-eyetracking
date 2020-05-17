import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import data


def plot_graph(data, trial_num):
    index = trial_num - 1
    m = data.get_movement()
    # print(m[0][1])
    # print(m[1][1])
    for i in range(len(m[0])):
        plt.plot(m[0][i], m[1][i])
    plt.show()

default_obj = data.read("test/asc/1211NE1.asc")
sess = default_obj.create_session()

plot_graph(sess, 1)
