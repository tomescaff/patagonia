import xarray as xr
import pandas as pd
import numpy as np

# compute numbers of days per month between init_date and end_date as xarray data array
def ndays_per_month(init_date = '1980-04-01', end_date = '2015-03-31'):
    
    # create daily serie of dates
    dr = pd.date_range(init_date, end_date)
    
    # create data array with 1's along time coordinate
    one_per_day = xr.DataArray( np.ones((dr.shape[0],)), coords=[dr], dims=['time'])

    # resample to monthly resolution
    ndays_per_month = one_per_day.resample(time='1MS').sum().sel(time=slice(init_date, end_date))
    return ndays_per_month

# transform monthly mean timeseries in [·/day] to monthly acc timeseries in [·/month]
# from_monthly_acc == True assumes input as a monthly acc timeseries in [·/month]
# use data from 1980-04 to 2015-03
def to_monthly_acc_values(da_monthly, from_monthly_acc = False, init_date = '1980-04-01', end_date = '2015-03-31'):

    # select time period
    da_monthly = da_monthly.sel(time=slice(init_date, end_date))

    # handle the case when input is already a monthly acc timeseries
    if from_monthly_acc: return da_monthly
    
    # get numbers of days per month
    ndays_month = ndays_per_month()
    
    # compute acc monthly serie
    da_monthly = da_monthly*ndays_month 
    return da_monthly

# transform monthly mean timeseries in [·/day] to yearly acc timeseries in [·/year]
# from_monthly_acc == True assumes input as a monthly acc timeseries in [·/month]
# use data from 1980-04 to 2015-03
def to_yearly_acc_values(da_monthly, from_monthly_acc = False):

    return to_monthly_acc_values(da_monthly, from_monthly_acc).resample(time='12MS').sum('time',skipna=False)
    
# transform monthly mean timeseries in [·/day] to yearly mean timeseries in [·/day]
# from_monthly_acc == True assumes input as a monthly acc timeseries in [·/month]
# use data from 1980-04 to 2015-03
def to_yearly_mean_values(da_monthly, from_monthly_acc = False):

    # to monthly acc timeseries in [·/month]
    da_monthly_acc = to_monthly_acc_values(da_monthly,  from_monthly_acc)
    
    # compute numbers of days per month in xarray
    ndays_month = ndays_per_month()
    
    # compute yearly acc serie
    yearly_data_acc = da_monthly_acc.resample(time='12MS').sum('time',skipna=False)
    ndays_per_year = ndays_month.resample(time='12MS').sum('time',skipna=False)

    # return yearly mean serie
    return yearly_data_acc/ndays_per_year

# transform monthly mean timeseries in [·/day] to winter acc timeseries in [·/winter]
# from_monthly_acc == True assumes input as a monthly acc timeseries in [·/month]
# use data from 1980-04 to 2015-03
def to_winter_acc_values(da_monthly, from_monthly_acc = False):

    da_seas = to_monthly_acc_values(da_monthly, from_monthly_acc).resample(time='6MS').sum('time',skipna=False)
    return da_seas[0::2]

# transform monthly mean timeseries in [·/day] to summer acc timeseries in [·/summer]
# from_monthly_acc == True assumes input as a monthly acc timeseries in [·/month]
# use data from 1980-04 to 2015-03
def to_summer_acc_values(da_monthly, from_monthly_acc = False):

    da_seas = to_monthly_acc_values(da_monthly, from_monthly_acc).resample(time='6MS').sum('time',skipna=False)
    return da_seas[1::2]

# transform monthly mean timeseries in [·/day] to winter mean timeseries in [·/day]
# from_monthly_acc == True assumes input as a monthly acc timeseries in [·/month]
# use data from 1980-04 to 2015-03
def to_winter_mean_values(da_monthly, from_monthly_acc = False):

    # to monthly acc timeseries in [·/month]
    da_monthly_acc = to_monthly_acc_values(da_monthly, from_monthly_acc)
    
    # compute numbers of days per month in xarray
    ndays_month = ndays_per_month()
    
    # compute winter acc serie
    winter_data_acc = da_monthly_acc.resample(time='6MS').sum('time',skipna=False)[0::2]
    ndays_per_year = ndays_month.resample(time='6MS').sum('time',skipna=False)[0::2]

    # return winter mean serie
    return winter_data_acc/ndays_per_year

# transform monthly mean timeseries in [·/day] to summer mean timeseries in [·/day]
# from_monthly_acc == True assumes input as a monthly acc timeseries in [·/month]
# use data from 1980-04 to 2015-03
def to_summer_mean_values(da_monthly, from_monthly_acc = False):

    # to monthly acc timeseries in [·/month]
    da_monthly_acc = to_monthly_acc_values(da_monthly, from_monthly_acc)
    
    # compute numbers of days per month in xarray
    ndays_month = ndays_per_month()
    
    # compute summer acc serie
    summer_data_acc = da_monthly_acc.resample(time='6MS').sum('time',skipna=False)[1::2]
    ndays_per_year = ndays_month.resample(time='6MS').sum('time',skipna=False)[1::2]

    # return summer mean serie
    return summer_data_acc/ndays_per_year
