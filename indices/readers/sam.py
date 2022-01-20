import pandas as pd
import xarray as xr
import numpy as np
from os.path import abspath, dirname, join

# path to the indices directory
INDICES_ROOT = dirname(dirname(abspath(__file__)))

# path to the folder with large scale indices
DATA_ROOT = join(INDICES_ROOT, 'data')

def aaoi_index():
    filepath = join(DATA_ROOT, 'monthly.aao.index.b79.current.ascii.txt')

    # read file as pandas dataframe
    df = pd.read_csv(filepath, header=None, sep='\s+')
    
    # get data 
    data = df.iloc[:,2].astype(float)

    # create and return xarray object with data
    init_date = str(df.iloc[0,0])+'-01-01'
    datetime = pd.date_range(start=init_date, periods=df.shape[0], freq='M')
    da = xr.DataArray(data.values, coords=[datetime], dims=['time'])
    da[da==-99.99] = np.nan
    return da