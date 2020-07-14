'''
Calculate CDFs for groundwater depth data in all wells usable for the model.
Generates a csv of location and CDF parameters for each well. Note that the equation
used for the CDF is a sigmoid of the form:

y = 1 / (1 + exp(-b * (x-a)))

where a and b are free parameters to be optimized, x is the groundwater DEPTH below NAVD88 elevation 
and y is the expected percentage of time where groundwater is present at this depth.
'''

import pandas as pd
import numpy as np
from scipy.optimize import curve_fit

def sanitize_latlon(x):
    '''
    Converts concatenated coordinates of the form
    DDMMSS.ssss... to decimal degrees.
    '''
    deg = x // 10000
    x -= deg * 10000

    min = x // 100
    x -= min * 100

    sec = x

    return deg + (min / 60) + (sec / 3600)

def sigmoid(x, a, b):
    '''
    Compute a logistic curve.
    '''
    return 1.0 / (1 + np.exp(-b * (x-a)))

def get_cdf_parameters(x):
    '''
    Compute parameters a and b for a cumulative distribution function
    represented by a sigmoidal curve (above function)
    '''
    N = len(x)

    x_sort = np.sort(x)
    cdf = np.array(range(N)) / float(N)

    popt, _ = curve_fit(sigmoid, x_sort, cdf)
    return popt

if __name__ == '__main__':
    wells = pd.read_csv('wells.csv')
    a_lis = []
    b_lis = []

    for idx, row in wells.iterrows():
        this_df = pd.read_csv('data/csvs/{}.csv'.format(row['Dbkey']))
        gwater_depths = -(this_df['gwater_elev_navd88'] - row['Elev_NAVD88']).dropna().to_numpy()
        a, b = get_cdf_parameters(gwater_depths)
        a_lis.append(a)
        b_lis.append(b)    

    all_data = pd.DataFrame({
        'dbkey': wells['Dbkey'],
        'latitude': wells['Latitude'].map(sanitize_latlon),
        'longitude': wells['Longitude'].map(sanitize_latlon) * -1, # E to W
        'x_coord': wells['X COORD'],
        'y_coord': wells['Y COORD'],
        'sigmoid_a': a_lis,
        'sigmoid_b': b_lis
    })

    all_data.to_csv('output.csv')