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

OUTPUT_LOC = r'U:\GIS\temp\KJG\fluccs\wells_output.csv"

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


def r_squared(a, b):
    '''
    Get the proportion of variance in a explained by b.
    '''
    SS_tot = np.sum(np.square(a - np.mean(a)))
    SS_res = np.sum(np.square(a - b))

    return 1 - (SS_res / SS_tot)


def get_cdf_parameters(x):
    '''
    Compute parameters a and b for a cumulative distribution function
    represented by a sigmoidal curve (above function)
    '''
    N = len(x)

    x_sort = np.sort(x)
    cdf = np.array(range(N)) / float(N)

    (a, b), _ = curve_fit(sigmoid, x_sort, cdf)
    r_sq = r_squared(cdf, sigmoid(x_sort, a, b))
    return a, b, r_sq


def process_df(row):
    this_df = pd.read_csv('data/csvs/{}.csv'.format(row['Dbkey']))
    gwater_depths = -(this_df['gwater_elev_navd88'] -
                      row['Elev_NAVD88']).dropna().to_numpy()
    return get_cdf_parameters(gwater_depths)


if __name__ == '__main__':
    wells = pd.read_csv('wells.csv')
    coeffs = wells.apply(
        process_df,
        axis=1,
        result_type='expand').rename(
        columns={0: 'sigmoid_a', 1: 'sigmoid_b', 2: 'sigmoid_r2'}
    )

    # Join the two dataframes together, rename last
    all_data = pd.concat([wells, coeffs], axis=1)

    all_data.to_csv(OUTPUT_LOC)
