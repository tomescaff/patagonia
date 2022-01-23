import pandas as pd
import xarray as xr
import numpy as np
from os.path import abspath, dirname, join

# path to the indices directory
INDICES_ROOT = dirname(dirname(abspath(__file__)))

# path to the folder with large scale indices
DATA_ROOT = join(INDICES_ROOT, 'data')

# useful for the majority of ENSO indices
def pdo_index():
    
    filepath = join(DATA_ROOT, 'ncdc_noaa_pdo_data.csv.txt')
    
    # read file as pandas dataframe
    df = pd.read_csv(filepath, header=0, sep=',', skiprows=1)
    
    # get data
    data = df['Value']
    
    # create date range
    dr = pd.date_range(start='1854-01-01', end='2019-07-31', freq='M')

    # create and return xarray object with data
    da = xr.DataArray(data, coords=[dr], dims=['time'])
    # da[da==nanvalue] = np.nan # handle nans
    return da