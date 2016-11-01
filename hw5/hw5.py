from geoplotter import GeoPlotter as Geo
import pandas
import scipy
import matplotlib
import matplotlib.pyplot
import networkx
import pyomo
import pyomo.opt
import pyomo.environ as pe


class Network:

    def __init__(self, fname):
        self.austin_df = pandas.read_csv(fname)
        self.adresses_df = pandas.read_csv('addresses.csv')
        self.geo = Geo()


        # Create the Network
        self.createNetworkxGraph()

        # Plot the basic map and adresses.
        # self.plotstreets(self.getPointsPlot(self.austin_df), 'Engineering Teaching Center',True, True)

