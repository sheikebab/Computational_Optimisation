import pandas as pd
import scipy
from geoplotter import GeoPlotter
import matplotlib
import matplotlib.cm
import matplotlib.pyplot as plt

# Create an object of the GeoPlotter class

world = GeoPlotter()

# Call the drawWorld function of class GeoPlotter

world.drawWorld()

# Reading the csv file into the program

nmc_df = pd.read_csv('NMC_v4_0.csv')
# print 'Imported data', nmc_df

# Function to get the cinc code when country code and year are specified.

def get_cinc(df, c_code, year):
    nmc_cinc = nmc_df[(df.ccode==c_code) & (df.year==year)]
    return nmc_cinc.cinc

# Testing the function to get the cinc

get_cinc(nmc_df, 2, 1896)

# Getting a list of all unique country codes

unique_ccode = nmc_df.year.unique()
# print 'List of al unique codes:\n', list(unique_ccode)

# Getting the value counts of all the country codes

value_count_ccode = nmc_df.ccode.value_counts(ascending=True)
# print 'Value counts of country codes:\n', value_count_ccode

# Reading in the cshapes file

c_shape = GeoPlotter()
c_shape.readShapefile('cshapes_0.4-2/cshapes', 'shape_file')

# Creating a Dataframe using the shapefile_info

c_shape_df = pd.DataFrame(c_shape.m.shape_file_info)
c_shape_df.head()

# Creating a function to get the indices of the desired country to later pass through the drawShapes function
# part of the GeoPlotter class
def get_indices(code_country):
    indices_country = scipy.array(0)

    for i in code_country:
        tmp = c_shape_df[c_shape_df.COWCODE == i].index.tolist()
        indices_country = scipy.append(indices_country, tmp)
    return indices_country.reshape(len(indices_country), 1)

idx = get_indices([2, 20])
# print idx

c_shape.drawWorld()
c_shape.drawShapes('shape_file', idx, facecolor='red')

# Define MilexPlotter class

class MilexPlotter(GeoPlotter):
    
    def __init__(self):
        self = GeoPlotter()
        self.nmc_df = pd.read_csv('NMC_v4_0.csv')
        self.readShapefile('cshapes_0.4-2/cshapes', 'shape_file_class')
        self.zorder == 0
        print self.m.shape_file_class_info
    
    def drawWorld(self):
        self.drawMapBoundary()
        self.fillContinents(color='blue')
        self.drawCoastLines(linewidth=0.7)
        self.drawCountries(linewidth=1.5)
        self.drawStates(linewidth=0.7)
        
    def plotCountry(self, code, **kwarg):
        self.readShapefile('cshapes_0.4-2/cshapes', 'shape_file_class')
        ind = get_indices(code)
        self.drawWorld()
        self.drawShapes('shape_file_class', ind, facecolor='red')
    
    # Mapping the cinc to colors
    def get_cinc_color(self, cinc_value):
        cinc_color = scipy.array(nmc_df.cinc)
        norm_cinc = matplotlib.colors.Normalize(vmin=0, vmax=cinc_color.max())
        cmap_r = matplotlib.cm.hot
        get_color = matplotlib.cm.ScalarMappable(norm=norm_cinc, cmap=cmap_r)
        return get_color.to_rgba(cinc_value)
        # print get_color.to_rgba(cinc_color)
        
    def plotYear(self, year_value, **kwargs):
        self.readShapefile('cshapes_0.4-2/cshapes', 'shape_file_class')
        self.nmc_df = pd.read_csv('NMC_v4_0.csv')
        tmp = nmc_df[nmc_df['year'] == year_value]
        tmp = tmp[['ccode', 'cinc']]
        tmp1 = tmp['ccode'].tolist()
        tmp2 = tmp['cinc'].tolist()
        indx = get_indices(tmp1).astype(int)
        self.drawWorld()
        self.drawShapes('shape_file_class', indx, **kwargs)

