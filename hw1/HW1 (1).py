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

