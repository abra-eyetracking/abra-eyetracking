import matplotlib.pyplot as plt
from PIL import Image
import data_test as dt
import numpy as np
class Visualization():
    data = dt.read("88001.asc")
    def fixation():
        plt.plot(data.movement[0])
        pt.plot(data.movement[1])


data = dt.read("88003.asc")

test_list = data.timestamps[]



range1 = int(data.trial_markers["end"][0]) - int(data.trial_markers["start"][0])
range2 = int(data.trial_markers["end"][1]) - int(data.trial_markers["start"][1])
index_x = np.array(data.movement[0][range1:range2+range1])
index_y = np.array(data.movement[1][range1:range2+range1])
index_x = index_x.astype(float).astype(int)
index_y = index_y.astype(float).astype(int)
pup = np.array(data.pupil_size[range1:range2+range1])
pup = pup.astype(float).astype(int)
print(max(index_x))
count = 0
for x in index_x:
    print(x)
fix_points = {}
# for fixa in

fig = plt.figure()
# plt.plot(data.movement[1][:range])
indexing = np.arange(range2)
print(indexing[::50])
# plt.yticks(indexing[::50])
# plt.show()
# xaxis = range(range)
plt.plot(indexing, index_x)
plt.plot(indexing, index_y)
fig2 = plt.figure()
plt.plot(indexing, pup)
fig3 = plt.figure()

img = Image.open('clip-art-clock-32.jpg')
img.thumbnail((1000, 1000), Image.ANTIALIAS)  # resizes image in-place
plt.imshow(img)
plt.plot(index_x, index_y)
plt.ylim(ymin = 0)
plt.ylim(ymax = max(index_y))
plt.show()
