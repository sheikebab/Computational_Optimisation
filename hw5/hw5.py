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

    def getPointsNetwork(self, ds):
        self.start_point = ds.kmlgeometry.str.extract('LINESTRING \(([0-9-.]* [0-9-.]*,)')
        self.end_point = ds.kmlgeometry.str.extract('([0-9-.]* [0-9-.]*)\)')
        return self.start_point, self.end_point

    def getPointsPlot(self, ds):
        self.start_point = scipy.array(ds.kmlgeometry.str.extract('LINESTRING \(([0-9-.]* [0-9-.]*,)'))
        self.end_point = scipy.array(ds.kmlgeometry.str.extract('([0-9-.]* [0-9-.]*)\)'))
        self.start_point = [i.split(' ') for i in self.start_point]
        self.end_point = [i.split(' ') for i in self.end_point]
        for i in range(len(self.start_point)):
            self.start_point[i][1] = self.start_point[i][1].replace(',', '')
        self.start_point = [[float(float(j)) for j in i] for i in self.start_point]
        self.end_point = [[float(float(j)) for j in i] for i in self.end_point]
        points = [[self.start_point[i], self.end_point[i]] for i in range(len(self.start_point))]
        return points

    def plotstreets(self, points, loc=None,  plotaddresses = False, plotgraph=False):

        self.geo.setZoom(-97.8526, 30.2147, -97.626, 30.4323)
        self.geo.drawLines(points, color = 'b',linewidth = 0.3)
        if plotaddresses:
            self.plotaddresses(self.adresses_df, loc)
        if plotgraph:
            matplotlib.pyplot.savefig('streets.png')
            matplotlib.pyplot.show()

    def plotaddresses(self, ds,  destination=None):

        for i in range(len(ds.Lon)):
            self.geo.drawPoints(ds.Lon[i], ds.Lat[i], color = 'r')
        if destination != None:
            Lat = ds[ds.Address.str.extract('([A-Za-z\- ]*),', expand=False) == destination][
                'Lat'].values[0]
            Lon = ds[ds.Address.str.extract('([A-Za-z\- ]*),', expand=False) == destination][
                'Lon'].values[0]
            self.geo.drawPoints(lat=Lat, lon=Lon, color='g')
            
    def getEdges(self):
        # Sets up edge sets
        # FT Streets
        FT_df = self.austin_df[self.austin_df.ONE_WAY == 'FT']
        FT_start, FT_end = self.getPointsNetwork(FT_df)
        FT_weights = [dict(weight=i) for i in FT_df.SECONDS.values]
        FT_edges = zip(FT_start, FT_end,FT_weights)

        # TF Streets
        TF_df = self.austin_df[self.austin_df.ONE_WAY == 'TF']
        TF_start, TF_end= self.getPointsNetwork(TF_df)
        TF_weights = [dict(weight=i) for i in TF_df.SECONDS.values]
        TF_edges = zip(TF_start, TF_end,TF_weights)

        # B Streets
        B_df = self.austin_df[self.austin_df.ONE_WAY == 'B']
        B_start, B_end = self.getPointsNetwork(B_df)
        B_weights = [dict(weight=i) for i in B_df.SECONDS.values]
        B_edges = zip(B_start, B_end,B_weights)

        return FT_edges, TF_edges, B_edges

