'''
Determine the proper cumulative probability distribution function for well groundwater
data.
'''
import pandas as pd 
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt 

data = pd.read_csv('data/csvs/L7448.csv')['gwater_elev_navd88'].dropna().to_numpy()

# Compute CDF by sorting the array and computing the proportion of data below each point
N = len(data)
data_sorted = np.sort(data)
cdf = np.array(range(N))/float(N)

#plt.plot(data_sorted, cdf)

# The data looks fairly normal and is scale (0, 1]. We can compute 
# a logistic curve to fit this data.
#https://stackoverflow.com/questions/4308168/sigmoidal-regression-with-scipy-numpy-python-etc
def sigmoid(x, a, b):
    '''
    Compute a logistic curve fitting
    '''
    y = 1.0 / (1 + np.exp(-b * (x-a)))
    return y

guess = np.median(data), np.median(cdf)
popt, _ = curve_fit(sigmoid, data_sorted, cdf)
print(popt)

a, b = popt
fitted = sigmoid(data_sorted, a, b)
plt.plot(data_sorted, cdf, 'red')
plt.plot(data_sorted, fitted, 'green')

plt.show()