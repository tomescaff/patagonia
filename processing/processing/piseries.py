from .settings import *
from .utils import icefields, resampling
from os.path import join
import pandas as pd
import xarray as xr

# load modeled variables over the patagonian icefields at monthly scale from plain text with final data
def load_piseries_monthly():
    mon_df = pd.read_csv('../data/month_piseries.txt', sep=';', parse_dates=['time'])
    varnames = ['mb', 'acc', 'abl', 'tas', 'pr', 'rsds']
    dataset_dict = {}
    for varname in varnames:
        dataset_dict[varname] = xr.DataArray(mon_df[varname], coords=[mon_df['time']], dims=['time'])
    return xr.Dataset(dataset_dict)

# load modeled variables over the patagonian icefields at yearly scale from plain text with final data
def load_piseries_yearly():
    mon_df = pd.read_csv('../data/year_piseries.txt', sep=';', parse_dates=['time'])
    varnames = ['mb', 'acc', 'abl', 'tas', 'pr', 'rsds']
    dataset_dict = {}
    for varname in varnames:
        dataset_dict[varname] = xr.DataArray(mon_df[varname], coords=[mon_df['time']], dims=['time'])
    return xr.Dataset(dataset_dict)


# return monthly timeseries of modeled variables over icefield (npi, spi, or both)
# this method is used for building the timeseries
def monthly_series(varname, icefield='both'):
    # check valid varnames
    assert varname in ['mb', 'acc', 'abl', 'tas', 'pr', 'rsds']
    # define filepath to model results
    npi = join(NPI_MODEL_RESULTS_ROOT, NPI_MODEL_RESULT_FILE)
    spi = join(SPI_MODEL_RESULTS_ROOT, SPI_MODEL_RESULT_FILE)
    # get monthly series and resample if necessary
    series = icefields.monthly_series(npi, spi, varname, icefield).sel(time=slice('1980-04-01', '2015-03-31'))
    if varname in ['mb', 'acc', 'abl', 'pr']:
        series = resampling.to_monthly_acc_values(series)
    return series

# return yearly timeseries of modeled variables over icefield (npi, spi, or both)
# this method is used for building the timeseries
def yearly_series(varname, icefield='both'):
    # check valid varnames
    assert varname in ['mb', 'acc', 'abl', 'tas', 'pr', 'rsds']
    # define filepath to model results
    npi = join(NPI_MODEL_RESULTS_ROOT, NPI_MODEL_RESULT_FILE)
    spi = join(SPI_MODEL_RESULTS_ROOT, SPI_MODEL_RESULT_FILE)
    # get yearly series and resample if necessary
    series = icefields.monthly_series(npi, spi, varname, icefield)
    if varname in ['mb', 'acc', 'abl', 'pr']:
        series = resampling.to_yearly_acc_values(series)
    else:
        series = resampling.to_yearly_mean_values(series)
    return series