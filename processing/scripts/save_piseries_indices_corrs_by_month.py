import pandas as pd
import numpy as np
import xarray as xr
from scipy import stats
from prepare_series import prepare_series

# compute date ranges for monthly correlation computing. See example below.
# x, y = dateranges_from_nominal_month_and_lag(4, 2)
# x == 1980-04, 1981-04, ... 2014-04
# y == 1980-06, 1981-06, ... 2014-06
def dateranges_from_nominal_month_and_lag(month, lag):
    mon_end = (month+lag-1)%12+1
    yea_off = (month+lag-1)//12
    if month >= 4:
        init_year = 1980
        end_year = 2014
    else:
        init_year = 1981
        end_year = 2015
    dr_x = pd.date_range(f'{init_year}-{month}-01',f'{end_year}-{month}-01', freq='12MS')
    dr_y = pd.date_range(f'{init_year+yea_off}-{mon_end}-01',f'{end_year+yea_off}-{mon_end}-01', freq='12MS')
    return dr_x, dr_y

# compute monthly correlation between x and y filtered by month (x) and month + lag (y)
def monthly_correlation_filtered_by_month(x, y, month, lag):
    
    # get dateranges
    dr_x, dr_y = dateranges_from_nominal_month_and_lag(month, lag)
    
    # dateranges to xarray dataarray
    dummy = np.zeros((35,))
    time_x = xr.DataArray(dummy, coords=[dr_x], dims=['time'])
    time_y = xr.DataArray(dummy, coords=[dr_y], dims=['time'])

    # fix times to fit in period (1980-04, 2015-03)
    if lag >= 0:
        time_y = time_y.sel(time=slice('1980-04-01', '2015-03-31')) 
        time_x = time_x[:time_y.size:]
    else:
        time_y = time_y.sel(time=slice('1980-04-01', '2015-03-31'))
        time_x = time_x[-time_y.size::]
    
    # filter series by times previously fixed
    x = x.sel(time = time_x.time)
    y = y.sel(time = time_y.time)

    # get r statistics with scipy pearsonr and return
    r, p = stats.pearsonr(x, y)
    return r, p

# create and save correlation tables between monthly anomalies series (x and y)
# filtered by month. Print tables to files in markdown format. 
def save_correlation_table(x, y, filepath_r, filepath_p):

    # month names  
    months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dec']

    # create tables as empty dataframes
    # r: Pearson's r coefficient
    # p: p-value
    mon_r_df = pd.DataFrame()
    mon_p_df = pd.DataFrame()

    # column 'lag' ranges from -6 until 6
    mon_r_df['lag'] = list(range(-6, 7))
    mon_p_df['lag'] = list(range(-6, 7))

    # compute monthly corrs filtered by month
    for m, month in enumerate(months):
        zipped = [monthly_correlation_filtered_by_month(x, y, m+1, lag) for lag in range(-6, 7)]
        rs, ps = zip(*zipped)
        mon_r_df[month] = rs
        mon_p_df[month] = ps
    
        # fill table with 2 decimal precision
        mon_r_df[month] = mon_r_df[month].apply(lambda x: round(x, 2))
        mon_p_df[month] = mon_p_df[month].apply(lambda x: round(x, 2))

    # start markdown conversion

    # colour significative correlations. 
    # if p < 0.05: r is red 
    # if 0.05 <= p < 0.1: r is blue.
    n, m = mon_r_df.shape
    for i in range(n):
        for j in range(1,m):
            if mon_p_df.iloc[i,j] < 0.05:
                mon_r_df.iloc[i,j] = '<span style="color: red">'+str(mon_r_df.iloc[i,j])+'</span>'
            if 0.05 <= mon_p_df.iloc[i,j] < 0.1:
                mon_r_df.iloc[i,j] = '<span style="color: blue">'+str(mon_r_df.iloc[i,j])+'</span>'

    # save r table
    with open(filepath_r, 'w') as f:
        print(mon_r_df.to_markdown(), file=f)
    # save p table
    with open(filepath_p, 'w') as f:
        print(mon_p_df.to_markdown(), file=f)

# define runs for creating and saving corr tables
runs = [
    ['enso-ep', 'mb', 'corr_mon_ensoep_mb'],
    ['enso-ep', 'tas', 'corr_mon_ensoep_tas'],
    ['enso-ep', 'pr', 'corr_mon_ensoep_pr'],

    ['enso-cp', 'mb', 'corr_mon_ensocp_mb'],
    ['enso-cp', 'tas', 'corr_mon_ensocp_tas'],
    ['enso-cp', 'pr', 'corr_mon_ensocp_pr'],

    ['enso-nino12', 'mb', 'corr_mon_enso12_mb'],
    ['enso-nino12', 'tas', 'corr_mon_enso12_tas'],
    ['enso-nino12', 'pr', 'corr_mon_enso12_pr'],

    ['sam', 'mb', 'corr_mon_sam_mb'],
    ['sam', 'tas', 'corr_mon_sam_tas'],
    ['sam', 'pr', 'corr_mon_sam_pr'],

    ['pdo', 'mb', 'corr_mon_pdo_mb'],
    ['pdo', 'tas', 'corr_mon_pdo_tas'],
    ['pdo', 'pr', 'corr_mon_pdo_pr'],

    ['enso-ep', 'sam', 'corr_mon_ensoep_sam'],
    ['enso-cp', 'sam', 'corr_mon_ensocp_sam'],

    ['enso-ep', 'enso-ep', 'corr_mon_ensoep_ensoep'],
    ['sam', 'sam', 'corr_mon_sam_sam'],

    ['enso-ep', 'abl', 'corr_mon_ensoep_abl'],
    ['enso-ep', 'acc', 'corr_mon_ensoep_acc'],
]

# get series of monthly anomalies 
data = prepare_series(detrend=False)

# create and save tables
for run in runs:
    save_correlation_table(data[run[0]], data[run[1]], '../data/corr_mon/'+run[2]+'_rval.md', '../data/corr_mon/'+run[2]+'_pval.md')
    