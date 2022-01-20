import xarray as xr
import pandas as pd
import numpy as np

# transform monthly mean timeseries in [·/day] to monthly acc timeseries in [·/month]
# use data from 1980-04 to 2015-03
def to_monthly_acc_values(da_monthly):
    # select time period
    da_monthly = da_monthly.sel(time=slice('1980-04-01', '2015-03-31'))
    
    # compute numbers of days per month in xarray
    dr = pd.date_range('1980-04-01','2015-03-31')
    one_per_day = xr.DataArray( np.ones((dr.shape[0],)), coords=[dr], dims=['time'])
    ndays_per_month = one_per_day.resample(time='1MS').sum().sel(time=slice('1980-04-01', '2015-03-31'))
    
    # compute acc monthly serie
    da_monthly = da_monthly*ndays_per_month 
    return da_monthly

# transform monthly mean timeseries in [·/day] to yearly acc timeseries in [·/year]
# use data from 1980-04 to 2015-03
def to_yearly_acc_values(da_monthly):
    return to_monthly_acc_values(da_monthly).resample(time='12MS').sum('time',skipna=False)
    
# transform monthly mean timeseries in [·/day] to yearly mean timeseries in [·/year]
# use data from 1980-04 to 2015-03
def to_yearly_mean_values(da_monthly):
    # select time period
    da_monthly = da_monthly.sel(time=slice('1980-04-01', '2015-03-31'))
    
    # compute numbers of days per month in xarray
    dr = pd.date_range('1980-04-01','2015-03-31')
    one_per_day = xr.DataArray( np.ones((dr.shape[0],)), coords=[dr], dims=['time'])
    ndays_per_month = one_per_day.resample(time='1MS').sum().sel(time=slice('1980-04-01', '2015-03-31'))
    
    # compute yearly mean serie
    da_monthly = da_monthly*ndays_per_month 
    yearly_data_acc = da_monthly.resample(time='12MS').sum('time',skipna=False)
    ndays_per_year = ndays_per_month.resample(time='12MS').sum('time',skipna=False)
    return yearly_data_acc/ndays_per_year
