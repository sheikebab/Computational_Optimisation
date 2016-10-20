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

