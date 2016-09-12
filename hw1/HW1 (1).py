import scipy
import pylab
from scipy.spatial.distance import squareform, pdist, cdist
import matplotlib.pylab as plt

# Creating a 3D array containing the coordinates (x,y) from the arrays X and Y

points = scipy.mgrid[0:20, 0:20]
coords = points.reshape(2, -1).T

