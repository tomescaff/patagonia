import xarray as xr
import numpy as np
import pandas as pd
from os.path import join
from .settings import *
from .utils import math

PRESSURE_LEVELS = [1000, 850, 700, 500, 300]

def get_stats_from_time_level_lat_lon_vars(series, filename, varname, mult, offset, resampling_fun, verbose = True, last_year_2014= False):

    # read netcdf variable as xarray data array
    basedir = ERAINT_MONTH_ROOT
    path = join(basedir, 'level', filename)
    da_lev = xr.open_dataset(path)[varname]

    # transform units using factor and offset
    da_lev = da_lev*mult+offset
    
    if verbose: print(varname)
    
    # case netcdf ends in 2014
    if last_year_2014: series = series.sel(time=slice('1980-04', '2014-03'))

    # compute stats for each pressure level
    stats = dict()
    for level in PRESSURE_LEVELS:
        if verbose: print(f'{level}')
        # select level
        da = da_lev.sel(level=level)

        # case netcdf ends in 2014
        if last_year_2014: da = da.sel(time=slice('1980-04', '2014-03'))

        # rename dimensions to common names
        da = da.rename({'latitude':'lat','longitude':'lon'})
        
        # adjust time resolution 
        da_resampled = resampling_fun(da)

        # compute stats between [time, lat, lon] and [time]
        regmap, pmap = math.regressmap_3D_1D_time_lat_lon(da_resampled,series)
        corrmap = math.correlation_3D_1D_time_lat_lon(da_resampled,series)
        
        # save in stats dict
        stats[varname+str(level)+'__regress'] = regmap
        stats[varname+str(level)+'__corr'] = corrmap
        stats[varname+str(level)+'__pvalue'] = pmap
    da_lev.close()
    return stats

def get_z_stats(series, resampling_fun, verbose = True):

    filename='zg_1979_2017_sellevels.nc'
    varname = 'z'
    mult = 1/9.8
    offset = 0 
    stats = get_stats_from_time_level_lat_lon_vars(series, filename, varname, mult, offset, resampling_fun, verbose)
    return stats

def get_t_stats(series, resampling_fun, verbose = True):

    filename='air_1979_2017.nc'
    varname = 't'
    mult = 1
    offset=-273.15
    stats = get_stats_from_time_level_lat_lon_vars(series, filename, varname, mult, offset, resampling_fun, verbose)
    return stats

def get_u_stats(series, resampling_fun, verbose = True):

    filename='uwnd_1979_2014_sellevels.nc'
    varname = 'u'
    mult = 1
    offset = 0 
    stats = get_stats_from_time_level_lat_lon_vars(series, filename, varname, mult, offset, resampling_fun, verbose, last_year_2014 = True)
    return stats

def get_v_stats(series, resampling_fun, verbose = True):

    filename='vwnd_1979_2014_sellevels.nc'
    varname = 'v'
    mult = 1
    offset = 0 
    stats = get_stats_from_time_level_lat_lon_vars(series, filename, varname, mult, offset, resampling_fun, verbose, last_year_2014 = True)
    return stats

def get_r_stats(series, resampling_fun, verbose = True):

    filename='rhum_1979_2014_sellevels.nc'
    varname = 'r'
    mult = 1
    offset = 0 
    stats = get_stats_from_time_level_lat_lon_vars(series, filename, varname, mult, offset, resampling_fun, verbose, last_year_2014 = True)
    return stats

def get_q_stats(series, resampling_fun, verbose = True):

    filename='q_1979_2014_sellevels.nc'
    varname = 'q'
    mult = 1000
    offset = 0 
    stats = get_stats_from_time_level_lat_lon_vars(series, filename, varname, mult, offset, resampling_fun, verbose, last_year_2014 = True)
    return stats

def get_sst_stats(series, resampling_fun, verbose = True):

    # read netcdf variable as xarray data array
    basedir = ERAINT_MONTH_ROOT
    filename='sst_1979_2017.nc'
    path = join(basedir, 'surface', filename)
    varname = 'sst'
    da = xr.open_dataset(path)[varname]
    
    # transform units using factor and offset
    mult = 1
    offset=-273.15 
    da = da*mult+offset

    if verbose: print(varname)
    
    # rename dimensions to common names
    da = da.rename({'latitude':'lat','longitude':'lon'})
    
    # create mask of not nulls (ocean)
    notnulls = da.mean('time').copy().notnull()

    # put 0's in land for resampling
    da = da.where(da.notnull(),0)
    
    # resample
    da_resampled = resampling_fun(da)

    # fill land grid cells with nans 
    da_resampled = da_resampled.where(notnulls, np.nan)
    
    # compute stats between [time, lat, lon] and [time]
    regmap, pmap = math.regressmap_3D_1D_time_lat_lon(da_resampled,series)
    corrmap = math.correlation_3D_1D_time_lat_lon(da_resampled,series)
    
    stats = dict()
    stats[varname+'__regress'] = regmap
    stats[varname+'__corr'] = corrmap
    stats[varname+'__pvalue'] = pmap
    da.close()

    return stats

def get_mslp_stats(series, resampling_fun, verbose = True):
    
    # read netcdf variable as xarray data array
    basedir = ERAINT_MONTH_ROOT
    filename='mslp_1979_2017.nc'
    path = join(basedir, 'surface', filename)
    varname = 'msl'
    da = xr.open_dataset(path)[varname]
    
    # transform units using factor and offset
    mult = 0.01
    offset = 0 
    da = da*mult+offset

    if verbose: print(varname)
    
    # rename dimensions to common names
    da = da.rename({'latitude':'lat','longitude':'lon'})
    
    # resample
    da_resampled = resampling_fun(da)

    # compute stats between [time, lat, lon] and [time]
    regmap, pmap = math.regressmap_3D_1D_time_lat_lon(da_resampled,series)
    corrmap = math.correlation_3D_1D_time_lat_lon(da_resampled,series)
    
    stats = dict()
    stats[varname+'__regress'] = regmap
    stats[varname+'__corr'] = corrmap
    stats[varname+'__pvalue'] = pmap
    da.close()
    return stats

def get_sat_stats(series, resampling_fun, verbose = True):
    
    # read netcdf variable as xarray data array
    basedir = ERAINT_MONTH_ROOT
    filename='t2m_1979_2017.nc'
    path = join(basedir, 'surface', filename)
    varname = 't2m'
    da = xr.open_dataset(path)[varname]
    
    # transform units using factor and offset
    mult = 1
    offset = -273.15 
    da = da*mult+offset

    if verbose: print(varname)
    
    # rename dimensions to common names
    da = da.rename({'latitude':'lat','longitude':'lon'})
    
    # resample
    da_resampled = resampling_fun(da)

    # compute stats between [time, lat, lon] and [time]
    regmap, pmap = math.regressmap_3D_1D_time_lat_lon(da_resampled,series)
    corrmap = math.correlation_3D_1D_time_lat_lon(da_resampled,series)
    
    stats = dict()
    stats[varname+'__regress'] = regmap
    stats[varname+'__corr'] = corrmap
    stats[varname+'__pvalue'] = pmap
    da.close()
    return stats

# Note: Eraint precip is stored as acc monthly data
def get_precip_stats(series, resampling_fun, verbose = True):
    
    # read netcdf variable as xarray data array
    basedir = ERAINT_MONTH_ROOT
    filename='erainterim-1979-2015-monthly-pr.nc'
    path = join(basedir, 'surface', filename)
    varname = 'tp'
    da = xr.open_dataset(path, decode_times=False)[varname]
    
    # transform units using factor and offset
    mult = 1000
    offset = 0 
    da = da*mult+offset

    # handling time coordinate
    da['time'] = pd.date_range('1979-01', '2015-12', freq='1MS')

    if verbose: print(varname)
    
    # rename dimensions to common names
    da = da.rename({'latitude':'lat','longitude':'lon'})
    
    # resample
    da_resampled = resampling_fun(da)

    # compute stats between [time, lat, lon] and [time]
    regmap, pmap = math.regressmap_3D_1D_time_lat_lon(da_resampled,series)
    corrmap = math.correlation_3D_1D_time_lat_lon(da_resampled,series)
    
    stats = dict()
    stats[varname+'__regress'] = regmap
    stats[varname+'__corr'] = corrmap
    stats[varname+'__pvalue'] = pmap
    da.close()
    return stats

# TODO: verify how pw is stored in Eraint monthly data (mean or acc)
def get_pw_stats(series, resampling_fun, verbose = True):
    
    # read netcdf variable as xarray data array
    basedir = ERAINT_MONTH_ROOT
    filename='pw_1979_2017.nc'
    path = join(basedir, 'level', filename)
    varname = 'tcwv'
    da = xr.open_dataset(path)[varname]
    
    # transform units using factor and offset
    mult = 1
    offset = 0 
    da = da*mult+offset

    if verbose: print(varname)
    
    # rename dimensions to common names
    da = da.rename({'latitude':'lat','longitude':'lon'})
    
    # resample
    da_resampled = resampling_fun(da)

    # compute stats between [time, lat, lon] and [time]
    regmap, pmap = math.regressmap_3D_1D_time_lat_lon(da_resampled,series)
    corrmap = math.correlation_3D_1D_time_lat_lon(da_resampled,series)
    
    stats = dict()
    stats[varname+'__regress'] = regmap
    stats[varname+'__corr'] = corrmap
    stats[varname+'__pvalue'] = pmap
    da.close()
    return stats

# Note: NOAA and Eraint lat-lon grids are different
def get_olr_stats(series, resampling_fun, verbose = True):
    
    # read netcdf variable as xarray data array
    basedir = NOAA_MONTH_ROOT
    filename='olr.nc'
    path = join(basedir, 'level', filename)
    varname = 'olr'
    da = xr.open_dataset(path)[varname]
    
    # transform units using factor and offset
    mult = 1
    offset = 0 
    da = da*mult+offset

    if verbose: print(varname)
    
    # rename dimensions to special names
    da = da.rename({'lat':'lat_noaa','lon':'lon_noaa'})

    # resample
    da_resampled = resampling_fun(da)

    # compute stats between [time, lat, lon] and [time]
    regmap, pmap = math.regressmap_3D_1D_time_lat_lon(da_resampled,series)
    corrmap = math.correlation_3D_1D_time_lat_lon(da_resampled,series)
    
    stats = dict()
    stats[varname+'__regress'] = regmap
    stats[varname+'__corr'] = corrmap
    stats[varname+'__pvalue'] = pmap
    da.close()
    return stats