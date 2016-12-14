import sys
sys.path.append('../')

from calculateDistance import random_ts, standardize
import pickle

"""generate a new standardized random time series and store it.
"""

pickle.dump(standardize(random_ts(1)), open('input_ts.dat', 'wb+'))