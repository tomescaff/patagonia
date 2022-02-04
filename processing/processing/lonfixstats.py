import xarray as xr
import numpy as np
import pandas as pd
from os.path import join
from .settings import *
from .utils import math

def get_stats_from_time_level_lat_lon_vars(series, filename, varname, mult, offset, resampling_fun, sel_lon, verbose = True, last_year_2014= False):
    
    # read netcdf variable as xarray data array
    basedir = ERAINT_MONTH_ROOT
    path = join(basedir, 'level', filename)
    da_lev = xr.open_dataset(path)[varname]

    # transform units using factor and offset
    da_lev = da_lev*mult+offset

    # select from 1000 to 100 hPa
    da_lev = da_lev.sel(level=slice(100,1000))
    
    if verbose: print(varname)
    
    # case netcdf ends in 2014
    if last_year_2014: 
        series = series.sel(time=slice('1980-04', '2014-03'))
        da_lev = da_lev.sel(time=slice('1980-04', '2014-03'))

    # rename dimensions to common names
    da_lev = da_lev.rename({'latitude':'lat','longitude':'lon'})

    # reorder coordinates
    da_lev = da_lev.sel(lat=slice(None,None,-1))
    da_lev.coords['lon'] = (da_lev.coords['lon'] + 180) % 360 - 180
    da_lev = da_lev.sortby(da_lev.lon)

    # select longitude for transect 
    daband = da_lev.sel(lon=sel_lon,method='nearest')

    # adjust time resolution 
    da_resampled = resampling_fun(daband)

    # compute stats between [time, level, lat] and [time]
    regmap, pmap = math.regress_3D_1D_map_level_lat(da_resampled, series)
    corrmap = math.correlation_3D_1D_time_level_lat(da_resampled, series)
    
    # save in stats dict
    stats = dict()
    stats[varname + '__regress'] = regmap
    stats[varname + '__corr'] = corrmap
    stats[varname + '__pvalue'] = pmap
    stats[varname + '__mean'] = da_resampled.mean('time')
    da_lev.close()
    return stats

def get_z_stats(series, resampling_fun, sel_lon, verbose = True):
    
    filename='hgt_1979_2014.nc'
    varname = 'z'
    mult = 1/9.8
    offset = 0 
    stats = get_stats_from_time_level_lat_lon_vars(series, filename, varname, mult, offset, resampling_fun, sel_lon, verbose, last_year_2014 = True)
    return stats

def get_t_stats(series, resampling_fun, sel_lon, verbose = True):
    
    filename='air_1979_2014.nc'
    varname = 't'
    mult = 1
    offset=-273.15
    stats = get_stats_from_time_level_lat_lon_vars(series, filename, varname, mult, offset, resampling_fun, sel_lon, verbose, last_year_2014 = True)
    return stats

def get_u_stats(series, resampling_fun, sel_lon, verbose = True):

    filename='uwnd_1979_2014.nc'
    varname = 'u'
    mult = 1
    offset = 0 
    stats = get_stats_from_time_level_lat_lon_vars(series, filename, varname, mult, offset, resampling_fun, sel_lon, verbose, last_year_2014 = True)
    return stats

def get_v_stats(series, resampling_fun, sel_lon, verbose = True):

    filename='vwnd_1979_2014.nc'
    varname = 'v'
    mult = 1
    offset = 0 
    stats = get_stats_from_time_level_lat_lon_vars(series, filename, varname, mult, offset, resampling_fun, sel_lon, verbose, last_year_2014 = True)
    return stats

def get_r_stats(series, resampling_fun, sel_lon, verbose = True):

    filename='rhum_1979_2014.nc'
    varname = 'r'
    mult = 1
    offset = 0 
    stats = get_stats_from_time_level_lat_lon_vars(series, filename, varname, mult, offset, resampling_fun, sel_lon, verbose, last_year_2014 = True)
    return stats

def get_q_stats(series, resampling_fun, sel_lon, verbose = True):

    filename='q_1979_2014.nc'
    varname = 'q'
    mult = 1000
    offset = 0 
    stats = get_stats_from_time_level_lat_lon_vars(series, filename, varname, mult, offset, resampling_fun, sel_lon, verbose, last_year_2014 = True)
    return stats

def get_w_stats(series, resampling_fun, sel_lon, verbose = True):
    
    filename='wwind_1979_2017_100hpa_1000hpa.nc'
    varname = 'w'
    mult = 1
    offset = 0 
    stats = get_stats_from_time_level_lat_lon_vars(series, filename, varname, mult, offset, resampling_fun, sel_lon, verbose, last_year_2014 = True)
    return stats
