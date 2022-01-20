import pandas as pd
import xarray as xr
import numpy as np
from os.path import abspath, dirname, join

# path to the indices directory
INDICES_ROOT = dirname(dirname(abspath(__file__)))

# path to the folder with large scale indices
DATA_ROOT = join(INDICES_ROOT, 'data')

# useful for the majority of ENSO indices
def generic_reader(filepath, nanvalue):
    
    # read file as pandas dataframe
    df = pd.read_csv(filepath, header=None, sep='\s+', skiprows=1)
 
    # count until no year is left
    for i in range(df.shape[0]):
        try:
            year = float(df.iloc[i,0])
            assert year > 0
        except:
            break
    
    # get data
    data = df.iloc[0:i,1:].astype(float)
    
    # create date range
    iniyear = df.iloc[0,0]+'-01-01'
    endyear = df.iloc[i-1,0]+'-12-31'
    dr = pd.date_range(start=iniyear, end=endyear, freq='MS')

    # create and return xarray object with data
    da = xr.DataArray(data.values.ravel(), coords=[dr], dims=['time'])
    da[da==nanvalue] = np.nan # handle nans
    return da

# nino 1+2 index at monthly timescale
def nino12_index():
    filepath = join(DATA_ROOT, 'nino12.data.txt')
    return generic_reader(filepath, nanvalue=-99.99)

# nino 3.4 index at monthly timescale
def nino34_index():
    filepath = join(DATA_ROOT, 'nino34.data.txt')
    return generic_reader(filepath, nanvalue=-99.99)

# nino 4 index at monthly timescale
def nino4_index():
    filepath = join(DATA_ROOT, 'nino4.data.txt')
    return generic_reader(filepath, nanvalue=-99.99)

# oni index at monthly timescale
def oni_index():
    filepath = join(DATA_ROOT, 'oni.data.txt')
    return generic_reader(filepath, nanvalue=-99.9)

# tni index at monthly timescale
def tni_index():
    filepath = join(DATA_ROOT, 'tni.data.txt')
    return generic_reader(filepath, nanvalue=-99.99)

# cti index at monthly timescale
def cti_index():
    filepath = join(DATA_ROOT, 'cti.data.txt')

    # read file as pandas dataframe
    df = pd.read_csv(filepath, header=None, sep='\s+')
    
    # get data
    data = df.iloc[:,0].astype(float)
    
    # create and return xarray object with data
    datetime = pd.date_range(start='1845-01-01', periods=df.shape[0], freq='MS')
    da = xr.DataArray(data.values, coords=[datetime], dims=['time'])
    da[da==-99.99] = np.nan # handle nans
    return da

# eastern-pacific enso index at monthly timescale
def ep_nino_index():
    filepath =  join(DATA_ROOT, 'Monthly_EP_1948_01_2021_01.txt')

    # read file as pandas dataframe
    df = pd.read_csv(filepath, sep=':')

    # create date range
    dr = pd.date_range('1948-01','2021-01', freq='1MS') + pd.DateOffset(days=14)

    # create and return xarray object with data
    da = xr.DataArray( df['EP index'], coords=[dr], dims=['time'])
    return da

# central-pacific enso index at monthly timescale
def cp_nino_index():
    filepath =  join(DATA_ROOT, 'Monthly_CP_1948_01_2021_01.txt')

    # read file as pandas dataframe
    df = pd.read_csv(filepath, sep=':')

    # create date range
    dr = pd.date_range('1948-01','2021-01', freq='1MS') + pd.DateOffset(days=14)

    # create and return xarray object with data
    da = xr.DataArray( df[' CP index'], coords=[dr], dims=['time'])
    return da



