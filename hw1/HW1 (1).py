import scipy
import pylab
from scipy.spatial.distance import squareform, pdist, cdist
import matplotlib.pylab as plt

# Creating a 3D array containing the coordinates (x,y) from the arrays X and Y

points = scipy.mgrid[0:20, 0:20]
coords = points.reshape(2, -1).T

# Now Calculating the distance of each point from the point [0,0] or the first term

distance = squareform(pdist(coords))

# Plotting the graph of distances from [0, 0}, which is stored in the array Val

a = int(raw_input('Input x coordinate\n'))
b = int(raw_input('Input y coordinate\n'))


def plot_distance(x, y, **kwargs):
    index = 20*x+y
    Val = distance[index].reshape(20,20)
    plt.imshow(Val, **kwargs)
    return plt.show()

plot_distance(a, b)  # Define the kwargs here for type of graph required
crds = [[0,0], [5,5], [19,19], [0,19], [19,0]]
ccrds =[]

# Calculate index of each point in distance matrix
for x in crds:
    x1 = x[0]
    y1 = x[1]
    if x1 == 0:
        index1 = y1
    else:
        index1 = 20*x1+y1
