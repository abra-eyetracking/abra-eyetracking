import matplotlib.pyplot as plt
from matplotlib import image
import os

import numpy as np
from scipy.stats import kde
import trial
import session
import data


# create data
def get_x_y(data):
    # print(data)
    temp = []
    x = np.array([index_2[0] for index_1 in data for index_2 in index_1])
    for check in x:
        if(check >= 0):
            temp.append(check)
        else:
            temp.append(0)
            print(check)
    x = temp
    temp = []
    y = np.array([index_2[1] for index_1 in data for index_2 in index_1])
    for check in y:
        if(check >= 0):
            temp.append(check)
        else:
            temp.append(0)
            print(check)
    y = temp
    return np.array(x), np.array(y)

def draw_heatmap(fixations, dispsize, imagefile):

    x,y = get_x_y(fixations)
    x = x
    y = y

    # Evaluate a gaussian kde on a regular grid of nbins x nbins over data extents
    nbins=100
    k = kde.gaussian_kde([x,y])
    xi, yi = np.mgrid[x.min():x.max():nbins*1j, y.min():y.max():nbins*1j]
    print(np.vstack([xi.flatten(), yi.flatten()]))
    print('y\n\n', yi)
    zi = k(np.vstack([xi.flatten(), yi.flatten()]))

    # Make the plot
    print(xi)
    # plt.pcolormesh(x, y, zi.reshape(xi.shape), alpha = 0.5)
    # plt.xlim(0,1920)
    # plt.ylim(0,1080)
    plt.show()
    plt.plot(x,y)
    plt.show()

    # Change color palette
    # plt.pcolormesh(xi, yi, zi.reshape(xi.shape), cmap=plt.cm.Greens_r)
    # plt.show()

    # screen = np.zeros((dispsize[1], dispsize[0], 3), dtype='float32')
    # # if an image location has been passed, draw the image
    # if imagefile != None:
    #     # check if the path to the image exists
    #     if not os.path.isfile(imagefile):
    #         raise Exception("ERROR in draw_display: imagefile not found at '%s'" % imagefile)
    #     # load image
    #     img = image.imread(imagefile)
    #     #
    #     # # width and height of the image
    #     w, h = len(img[0]), len(img)
    #     # # x and y position of the image on the display
    #     x = int(dispsize[0] / 2 - w / 2)
    #     y = int(dispsize[1] / 2 - h / 2)
    #     # # draw the image on the screen
    #     print(y+h)
    #     screen[y:y + h, x:x + w,:] += img
    #
    # # dots per inch
    # dpi = 100.0
    # # determine the figure size in inches
    # figsize = (dispsize[0] / dpi, dispsize[1] / dpi)
    # # create a figure
    # fig = pyplot.figure(figsize=figsize, dpi=dpi, frameon=False)
    #
    # # ax.scatter(x, y, label=None,
    # #                c=np.log10(population), cmap='viridis',
    # #                s=area, linewidth=0, alpha=0.5)
    # #    ax.axis(aspect='equal')
    #
    # ax = pyplot.Axes(fig, [0, 0, 1, 1])
    # ax.set_axis_off()
    # fig.add_axes(ax)
    # # plot display
    # ax.axis([0, dispsize[0], 0, dispsize[1]])
    # ax.imshow(img)

# default_obj = data.read("1211NE1.asc")
# sess = default_obj.create_session()
# fixations = sess.get_fixation()
# print(np.array(fixations[3]).shape)
# # draw_heatmap(fixations[3], dispsize = (1920, 1080), imagefile = 'clip-art-clock-32.jpg')
# x,y = get_x_y(fixations[3])
# def f(x, y):
#     return np.sin(x) ** 10 + np.cos(10 + y * x) * np.cos(x)
# X, Y = np.meshgrid(x, y)
# Z = f(X, Y)
# plt.contourf(X, Y, Z, 20, cmap='RdGy')
# plt.colorbar()
# plt.xlim(0,1920)
# plt.ylim(0,1080)
# plt.show()
