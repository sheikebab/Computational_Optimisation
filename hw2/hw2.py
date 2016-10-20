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
