import os
import xarray as xr
import pandas as pd
from .settings import *

def load_extseries_monthly():
    filepath = '../data/month_extseries.txt'
    # read data
    mon_df = pd.read_csv(filepath, sep=';', parse_dates=['time'])
    # get varnames from dataframe columns
    varnames = list(mon_df.columns)
    varnames.remove('time')
    # create xarray dataset and return
    dataset_dict = {}
    for varname in varnames:
        dataset_dict[varname] = xr.DataArray(mon_df[varname], coords=[mon_df['time']], dims=['time'])
    return xr.Dataset(dataset_dict)

# define reg-scale boxes
BOXU850     = dict(latmin=-52,latmax=-46,lonmin=-75.5,lonmax=-74.5)
BOXSSTP     = dict(latmin=-52,latmax=-46,lonmin=-80,lonmax=-76)

# define large-scale boxes
BOXDRAKE    = dict(latmin=-68,latmax=-53,lonmin=-100,lonmax=-60)
BOXASL      = dict(latmin=-75,latmax=-60,lonmin=-150,lonmax=-100)
BOXSSTAUST  = dict(latmin=-65,latmax=-49,lonmin=150,lonmax=-140+360)
PACSUB      = dict(latmin=-40,latmax=-30,lonmin=-150,lonmax=-100)

# read from RegCM files
def read_regcm4(varname, vartype, scale, offset, arglatlon, nomean = False):
    # vartype is no longer used
    multifile_path = f'{REGCM_MONTH_ROOT}/{varname}/*.nc'
    ds = xr.open_mfdataset(multifile_path, combine='by_coords')
    da = ds[varname]*scale + offset
    dabox = da.sel(lat=slice(arglatlon['latmin'],arglatlon['latmax']),
                   lon=slice(arglatlon['lonmin'],arglatlon['lonmax']))
    if nomean:
        return dabox
    dabox = dabox.mean(['lat','lon'])
    dabox.load()
    return dabox.squeeze()

# read from Era-Interim files
def read_eraint(filename, varname, vartype, scale, offset, arglatlon, level = None, nomean = False):
    path = os.path.join(ERAINT_MONTH_ROOT, vartype, filename)
    da = xr.open_dataset(path)[varname]*scale+offset
    if level is not None:
        da = da.sel(level=level)
    da = da.rename({'latitude':'lat','longitude':'lon'})
    da = da.sel(lat=slice(None, None,-1))
    da = da.assign_coords(lon=(((da.lon + 180) % 360) - 180))
    da = da.sortby(da.lon)
    dabox = da.sel(lat=slice(arglatlon['latmin'],arglatlon['latmax']),
                   lon=slice(arglatlon['lonmin'],arglatlon['lonmax']))
    if nomean:
        return dabox
    dabox = dabox.mean(['lat','lon'])
    dabox.load()
    return dabox.squeeze()

# Western Patagonia fjiord time series

def u850_pat(arglatlon=BOXU850, nomean=False):
    return read_regcm4('ua850', 'level', 1, 0, arglatlon, nomean=nomean)
    
def t850_pat(arglatlon=BOXU850):
    return read_regcm4('ta850', 'level', 1, -273.15, arglatlon)
    
def v850_pat(arglatlon=BOXU850):
    return read_regcm4('va850', 'level', 1, 0, arglatlon)

def q850_pat(arglatlon=BOXU850):
    return read_regcm4('hus850', 'level', 1, 0, arglatlon)

# Western Patagonia off shore time series

def evap_pat(arglatlon=BOXSSTP):
    return read_regcm4('evspsbl', 'surface', 3600*24, 0, arglatlon)

def huss_pat(arglatlon=BOXSSTP):
    return read_regcm4('huss', 'surface', 3600*24, 0, arglatlon)

def sensible_pat(arglatlon=BOXSSTP):
    return read_regcm4('hfss', 'surface', 1, 0, arglatlon)

def rsnl_pat(arglatlon=BOXSSTP):
    return read_regcm4('rsnl', 'surface', 1, 0, arglatlon)

def sst_pat(arglatlon=BOXSSTP):
    filename = 'sst_1979_2017.nc'
    return read_eraint(filename, 'sst', 'surface', 1, -273.15, arglatlon)

# Drake time series

def z300_drake(arglatlon=BOXDRAKE):
    filename = 'zg300_1979_2017.nc'
    return read_eraint(filename, 'z', 'level', 1/9.8, 0, arglatlon, level = 300)

def z500_drake(arglatlon=BOXDRAKE):
    filename = 'zg500_1979_2017.nc'
    return read_eraint(filename, 'z', 'level', 1/9.8, 0, arglatlon, level = 500)

def z700_drake(arglatlon=BOXDRAKE, nomean=False):
    filename = 'zg700_1979_2017.nc'
    return read_eraint(filename, 'z', 'level', 1/9.8, 0, arglatlon, level = 700, nomean=nomean)

def sst_drake(arglatlon=BOXDRAKE, nomean=False):
    filename = 'sst_1979_2017.nc'
    return read_eraint(filename, 'sst', 'surface', 1, -273.15, arglatlon, nomean=nomean)

def t700_drake(arglatlon=BOXDRAKE, nomean=False):
    filename = 'air_1979_2017.nc'
    return read_eraint(filename, 't', 'level', 1/9.8, 0, arglatlon, level = 700, nomean=nomean)

def t850_drake(arglatlon=BOXDRAKE, nomean=False):
    filename = 'air_1979_2017.nc'
    return read_eraint(filename, 't', 'level', 1/9.8, 0, arglatlon, level = 850, nomean=nomean)


# Other large-scale time series

def asl_mean(arglatlon=BOXASL):
    filename = 'mslp_1979_2017.nc'
    return read_eraint(filename, 'msl', 'surface', 0.01, 0, arglatlon)

def sst_pacsub(arglatlon=PACSUB):
    filename = 'sst_1979_2017.nc'
    return read_eraint(filename, 'sst', 'surface', 1, -273.15, arglatlon)

def sst_australia(arglatlon=BOXSSTAUST):
    filename = 'sst_1979_2017.nc'
    return read_eraint(filename, 'sst', 'surface', 1, -273.15, arglatlon)


    

