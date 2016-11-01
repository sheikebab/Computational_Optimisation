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

    def createNetworkxGraph(self):
        self.network = networkx.DiGraph()
        FT, TF, B = self.getEdges()
        self.network.add_edges_from(FT)
        self.network.add_edges_from(TF)
        self.network.add_edges_from(B)

   
    def findClosestNode(self, Lat,Lon):
        pos_nodes = scipy.array([])
        range_lat = [min([z[1][1] for z in self.getPointsPlot(self.austin_df)]),
                max([z[1][1] for z in self.getPointsPlot(self.austin_df)])]
        range_lon = [min([z[1][0] for z in self.getPointsPlot(self.austin_df)]),
                max([z[1][0] for z in self.getPointsPlot(self.austin_df)])]
        latdf = 0.0005
        londf = 0.0005
        ct = 0
        list_Lon = scipy.array([z[1][0] for z in self.getPointsPlot(self.austin_df)])
        list_Lat = scipy.array([z[1][1] for z in self.getPointsPlot(self.austin_df)])

        while len(pos_nodes) == 0 and ((latdf < scipy.absolute(range_lat[0] - range_lat[1]) / 2) and (
            londf < scipy.absolute(range_lon[0] - range_lon[1]))):
            ct = ct + 1
            latidx1 = scipy.where((list_Lat < Lat + ct * latdf))
            tempLatList = list_Lat[latidx1]
            tempLonList = list_Lon[latidx1]
            latidx = scipy.where(tempLatList > Lat - ct * latdf)
            tempLatList = tempLatList[latidx]
            tempLonList = tempLonList[latidx]
            lonidx1 = scipy.where(tempLonList > Lon - ct * londf)
            tempLatList = tempLatList[lonidx1]
            tempLonList = tempLonList[lonidx1]
            lonidx = scipy.where(tempLonList < Lon + ct * londf)
            pos_nodes = scipy.array([tempLonList[lonidx], tempLatList[lonidx]])

        if len(pos_nodes) == 0:
            return None
        else:
            dist = scipy.sqrt(scipy.sum(scipy.array([pos_nodes[0] - Lon, pos_nodes[1] - Lat]) ** 2, axis=0))
            closeNode = scipy.array([pos_nodes[0][scipy.where(dist == min(dist))][0],
                                     pos_nodes[1][scipy.where(dist == min(dist))][0]])
            nodeNames = [z[0] for z in self.getPointsPlot(self.austin_df) if (z[1][0] == closeNode[0]) & (z[1][1] == closeNode[1])]
            return nodeNames

    def getSPNDjikstras(self, start_node, dest_node):
        return networkx.shortest_path(self.network, source=start_node, target=dest_node)

